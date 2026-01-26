#-----------------------------------------------------------------------------------
# 작성자: 3002 기동주
# 작성 목적: [파이썬 1일차 - Codelab ②]: 대용량 데이터 파이프라인의 메모리 프로파일링
#                                     대규모 데이터 처리 시 하드웨어 자원을 효율적으로 사용
# 작성일: 2026.01.24
#
# 변경사항 내역(날짜, 변경목적, 변경내용 순으로 기입)
#-----------------------------------------------------------------------------------
# 실습 가이드
# 1,000만 개의 정수 데이터를 처리할 때 List Comprehension과 Generator Expression의 
# 메모리 점유율을 tracemalloc으로 측정
#
# 결과를 통해 파이썬의 'Lazy Evaluation(지연 평가)' 원리를 설명
#
# 라이브러리
# import tracemalloc
#-----------------------------------------------------------------------------------


import tracemalloc
import gc
import time

N = 10_000_000

# 메모리 상태 출력용 함수
def report(label: str):
    current, peak = tracemalloc.get_traced_memory()
    print(f"{label:<30} | current={current:>15} bytes | peak={peak:>15} bytes")



def list_comprehension():
    print("\nList Comprehension")
    # 이전 실행이나 다른 객체가 남긴 영향을 줄여 
    # “start” 시점의 상태를 최대한 비슷하게 만들기 위함
    gc.collect()
    tracemalloc.start()
    report("start")

    t0 = time.perf_counter()
    lsit_comp = [i for i in range(N)]
    report("리스트 생성 이후")

    total = sum(lsit_comp)
    t1 = time.perf_counter()
    report("리스트 합 연산 이후")

    # 참고: 리스트를 제거하면 메모리가 줄어드는지도 실험 해보기
    del lsit_comp
    gc.collect()
    report("제거 + 정리 이후")

    tracemalloc.stop()
    print(f"sum={total}, time={t1 - t0:.2f}s")

def generator_Expression():
    print("\nGenerator Expression")
    gc.collect()
    tracemalloc.start()
    report("start")

    t0 = time.perf_counter()
    gen = (i for i in range(N))
    report("제너레이터 생성 이후")

    total = sum(gen)
    t1 = time.perf_counter()
    report("제너레이터 합 연한 이후")

    # gen은 생성해도 메모리를 거의 차지 안함
    del gen
    gc.collect()
    report("제거 + 정리 이후")

    tracemalloc.stop()
    print(f"sum={total}, time={t1 - t0:.2f}s")

def main():
    list_comprehension()
    generator_Expression()

if __name__ == "__main__":
    main()


#===========================================================================================
#===============파이썬의 'Lazy Evaluation(지연 평가)' 원리=====================================
#
# List Comprehension 은 N개 전부를 즉시 생성해서 리스트에 저장한다.
# 정수 객체와 리스트의 포인터 배열까지 한 번에 메모리에 저장된다.
# 따라서 리스트 생성 이후에 409087104 bytes 까지 peak 메모리가 늘어난다.
#
# 반면 Generator Expression 은 생성 지점에 10_000_000 가 넘는 컨테이너 없이
# sum(gen)에서 필요할 때 마다 (생성 -> 연산 -> 버리기) 흐름이기 때문에 메모리를 적게 차지한다.
#
# 즉, Lazy Evaluation은 “필요할 때만 값을 계산하고, 계산한 값도 즉시 소비해서 쌓아두지 않는 방식이다.
# 대규모 데이터 처리 시 하드웨어 자원을 효율적으로 사용할 수 있다.
#===========================================================================================