#-----------------------------------------------------------------------------------
# 작성자: 3002 기동주
# 작성 목적: [파이썬 2일차 Codelab_1 - 병렬 데이터 마스킹 및 텍스트 정규화(Normalization) ]
#           CPU 바운드 작업의 병렬화 한계를 이해
#           대규모 트래픽 데이터에서 개인정보 및 부적절한 데이터를 정제하는 고성능 파이프
#           라인을 설계
# 작성일: 2026.01.31
#
# 변경사항 내역(날짜, 변경목적, 변경내용 순으로 기입)
#-----------------------------------------------------------------------------------
# • 실습 가이드
#   ‣ 시나리오
#       수백만 건의 사용자 리뷰 데이터 내에 포함된 이메일 주소,
#       전화번호 등의 개인정보를 마스킹(****) 처리하고,
#       특정 금칙어를 표준 표현으로 순화하는 배치 프로세서를 구축
# • 핵심 포인트
#   ‣ 정규표현식(Regex)의 오버헤드
#     복잡한 정규표현식은 CPU 자원을 많이 소모
#     이를 멀티 프로세스로 분산했을 때의 성능 이득을 확인
#   ‣ 데이터 청킹(Chunking)
#     500만 건의 데이터를 리스트 하나로 처리할 때와
#     코어 수만큼 나눠서 병렬 처리할 때의 처리량(Throughput) 차이를 분석
#   ‣ IPC 비용
#     데이터가 너무 작으면 프로세스 간 통신(IPC) 비용이
#     실행 시간보다 커질 수 있음을 이해
#-----------------------------------------------------------------------------------

import re
import json
import time
from dataclasses import dataclass
from multiprocessing import Pool, cpu_count
from typing import Pattern, Iterable, Iterator, Dict, List

#================================참고사항===================================
# - 코드에 사용한 데이터 셋은 yelp에서 다운로드 가능한 open dataset을 사용.
# - dataset의 여러 data 중에서 yelp_academic_dataset_review.json 파일을 사용하였고, 
#   key는 "review_id", "user_id", "text" 3가지 를 선택하여 전처리한 파일을 사용.
# - 출처: https://business.yelp.com/data/resources/open-dataset/
# 
# - 마스킹과 금칙어 순화 작업을 완료하면 process 종류에 따라 output_single.jsonl 과 
#   output_multi.jsonl 에 저장.
#
# - 파일 앞에서 원하는 개수 만큼 자르기: head -n 원하는개수 원본파일명.jsonl > 새로만들파일명.jsonl
#==========================================================================

#==========================================================================
# 1. 정규식, 금칙어 규칙
#==========================================================================
ID_LEN = 22 # id 길이 22자리로 고정된 데이터 사용
KEEP = 4    # 앞 4자리 제외하고 전부 마스킹 처리 예정

MASK_REVIEW_ID = re.compile(rf'^(.{{{KEEP}}})(.{{{ID_LEN-KEEP}}})$')
MASK_USER_ID = re.compile(rf'^(.{{{KEEP}}})(.{{{ID_LEN-KEEP}}})$')


# 데이터 클래스로 rule 관리
@dataclass(frozen=True)
class ProfanityRule:
    word: str
    pattern: Pattern[str]
    replace: str

PROFANITY_RULES = [
    ProfanityRule("fuck", re.compile(r"\bfuck\b", re.IGNORECASE), "f-word"),
    ProfanityRule("shit", re.compile(r"\bshit\b", re.IGNORECASE), "s-word"),
    ProfanityRule("asshole", re.compile(r"\basshole\b", re.IGNORECASE), "a-word"),
    ProfanityRule("bitch", re.compile(r"\bbitch\b", re.IGNORECASE), "b-word"),
    ProfanityRule("bastard", re.compile(r"\bbastard\b", re.IGNORECASE), "b-word"),
    ProfanityRule("dick", re.compile(r"\bdick\b", re.IGNORECASE), "d-word"),
    ProfanityRule("cunt", re.compile(r"\bcunt\b", re.IGNORECASE), "c-word"),
    ProfanityRule("damn", re.compile(r"\bdamn\b", re.IGNORECASE), "d-word"),
    ProfanityRule("hell", re.compile(r"\bhell\b", re.IGNORECASE), "h-word"),
    ProfanityRule("crap", re.compile(r"\bcrap\b", re.IGNORECASE), "c-word"),
    ProfanityRule("jerk", re.compile(r"\bjerk\b", re.IGNORECASE), "j-word"),
]

#==========================================================================
# 2. 텍스트 마스킹, 정규화
#==========================================================================
def mask_nomalize(review_id:str, user_id:str, text:str, rules: Iterable[ProfanityRule] = PROFANITY_RULES)->str:
    # ID 마스킹
    masked_review_id = MASK_REVIEW_ID.sub(lambda m: m.group(1) + '*' * len(m.group(2)), review_id)
    masked_user_id = MASK_USER_ID.sub(lambda m: m.group(1) + '*' * len(m.group(2)), user_id)
    
    # 텍스트(리뷰) 정규화 루프
    out = text
    for rule in rules:
        out = rule.pattern.sub(rule.replace, out)
    
    return  masked_review_id, masked_user_id, out

def mask_nomalize_record(rec:Dict, rules: Iterable[ProfanityRule] = PROFANITY_RULES)->Dict:
    review_id = rec.get("review_id", "") # 혹시 key가 없는 경우 빈 문자열로 대체
    user_id = rec.get("user_id", "")
    text = rec.get("text", "")

    masked_review_id, masked_user_id, text_norm = mask_nomalize(review_id, user_id, text, rules)

    out = dict(rec) # 원본 보존을 위해 복사
    out["review_id"] = masked_review_id
    out["user_id"] = masked_user_id
    out["text"] = text_norm

    return out


#==========================================================================
# 3. JSONL 파일 스트리밍 I/O 및 청킹
#==========================================================================

# 파일을 한 줄씩 읽어오기
def read_jsonl(path:str)->Iterator[dict]:
    with open(path, encoding="utf-8") as j:
        for line in j:
            line = line.strip()
            yield json.loads(line)


def write_jsonl(path:str, write: Iterator[dict]):
    count = 0
    with open(path, "w", encoding = "utf-8") as j:
        for count, w in enumerate(write, start=1):
            j.write(json.dumps(w, separators=(",", ":")))
            j.write("\n")
    return count    

# chunk_size 대로 묶어서 리스트를 반환
def chunking(iter: Iterator[dict], chunk_size: int)->Iterator[List[dict]]:
    buffer:List[dict] = []

    for rec in iter:
        buffer.append(rec)
        if len(buffer) >= chunk_size:
            yield buffer
            buffer = []

    # 버퍼에 남은 나머지도 처리
    if buffer:
        yield buffer    

#==========================================================================
# 4. single process
#==========================================================================
def single_process(path_input:str, path_output:str)->int:
    def gen():
        for i in read_jsonl(path_input):
            yield mask_nomalize_record(i)
    
    return write_jsonl(path_output, gen())
#==========================================================================
# 5. multi process
#==========================================================================

# worker가 실행할 단위 함수 정의
def chunk_process(chunk:List[dict])->List[dict]:

    out: List[dict] = []

    for i in chunk:
        out.append(mask_nomalize_record(i))
    return out

def multi_process(path_input:str, path_output:str, core: int, chunk_size: int)->int:

    chunk = chunking(read_jsonl(path_input), chunk_size)

    def gen():
        with Pool(processes=core) as pool:
            for i in pool.imap(chunk_process, chunk, chunksize=1):
                for rec in i:
                    yield rec

    return write_jsonl(path_output, gen())
#==========================================================================
# 6. 실행 시간 측정
#==========================================================================
def benchmark(func, *args, **kwargs):
    t0 = time.perf_counter()
    n = func(*args, **kwargs)
    t1 = time.perf_counter()
    elapsed = t1 - t0
    throughput = (n / elapsed) if elapsed > 0 else float("inf")
    return n, elapsed, throughput

#==========================================================================
# 7. 처리 결과 검증
#==========================================================================
# 마스킹 결과 
def head_jsonl(path: str, n: int = 5) -> List[dict]:
    out = []
    for i, rec in enumerate(read_jsonl(path)):
        if i >= n:
            break
        out.append(rec)
    return out

# 대체된 금칙어 검증
def find_replacements(path_in: str, limit_scan: int = 2000, max_print: int = 3) -> None:
    printed = 0
    for i, rec in enumerate(read_jsonl(path_in)):
        if i >= limit_scan:
            break

        before = rec.get("text", "")
        after_rec = mask_nomalize_record(rec)
        after = after_rec.get("text", "")

        if before != after:
            print("\n[profanity replaced]")
            print("before:", before[:1000])
            print("after :", after[:1000])
            printed += 1
            if printed >= max_print:
                break
#==========================================================================
# 8. main 실행
#==========================================================================

if __name__ == "__main__":

    path_in = "/home/epk0930/SKALA/Python/codelab3/review_5m.jsonl"
    path_out_single = "/home/epk0930/SKALA/Python/codelab3/output_single.jsonl"
    path_out_multi = "/home/epk0930/SKALA/Python/codelab3/output_multi.jsonl"

    workers = max(1, cpu_count() - 1)
    chunk_size = 20000

    n_s, elapsed_s, throughput_s = benchmark(single_process, path_in, path_out_single)
    n_m, elapsed_m, throughput_m = benchmark(multi_process, path_in, path_out_multi, workers, chunk_size)


    print("\n=== masking check ===")
    print("\n[masked ID: single-process]")
    for rec in head_jsonl(path_out_single, 5):
        print("review_id:", rec.get("review_id"), "user_id:", rec.get("user_id"))

    print("\n[masked ID: multi-process]")
    for rec in head_jsonl(path_out_multi, 5):
        print("review_id:", rec.get("review_id"), "user_id:", rec.get("user_id"))

    print("\n=== profanity replacement check  ===")
    find_replacements(path_in, limit_scan=5000, max_print=3)

    print("\n=== process summary ===")
    print(f"[single-process] records={n_s} elapsed={elapsed_s:.4f}s throughput={throughput_s:,.0f} rec/s")
    print(f"[multi-process]  records={n_m} elapsed={elapsed_m:.4f}s throughput={throughput_m:,.0f} rec/s workers={workers} chunk_size={chunk_size}")

    speedup = elapsed_s / elapsed_m if elapsed_m > 0 else float("inf")
    tput_gain = throughput_m / throughput_s if throughput_s > 0 else float("inf")

    print("\n=== performance analysis ===")
    print(f"speedup: {speedup:.2f}x  (multi-process is {speedup:.2f}x faster than single-process)")

#===============================================================================================================
# 결과 분석
#===============================================================================================================
# 1. 데이터가 500개로 매우 작은 경우
#    데이터가 매우 작으면 IPC 비용이 실행 시간 보다 커지는 경우가 있었다.
#    worker = 7 으로 설정해 놓고 chunk_size 가 100인 경우와 200인 경우 결과가 달랐다.
#    chunk_size = 200인 경우 multi-process가 single-process 보다 더 느렸고,
#    chunk_size = 100인 경우 multi-process가 더 빨랐다.
#    따라서 여기서 배운 점은 데이터가 작을수록 IPC 및 병렬화의 오버헤드가 전체 실행 시간에서 차지하는 비율이
#    커지며, 이로 인해 multi processing 성능이 불안정해질 수 있다는 점이다.
#
# 2. 데이터가 5_000_000개로 큰 경우
#    먼저 50만 건의 데이터로 chunk_size = 10000, 20000, 40000 을 비교하여 가장 시간이 적게 걸린
#    20000을 chunk_size로 두고 500만 건을 처리한 결과 
#    single-process는 처리시간: 612.6454초, 처리량: 8161 rec/s
#    multi-process 는 처리시간: 227.1028초, 처리량: 22016 rec/s
#    로, 처리 성능이 약 2.7배 향상되었음을 확인하였다.
