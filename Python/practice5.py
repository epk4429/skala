#---------------------------------------------------------------------------
# 작성자: 3002 기동주
# 작성 목적: [파이썬 2일차 실습 - multiprocessing으로 대용량 데이터 처리 ]
#           Python의 multiprocessing 모듈을 활용하여 CPU 병렬 처리 구조 이해
#           대용량 연산을 병렬화하여 처리 시간 비교 실험
#           Process, Queue, Pool 구조 이해 및 응용
# 작성일: 2026.01.26
#
# 변경사항 내역(날짜, 변경목적, 변경내용 순으로 기입)
#---------------------------------------------------------------------------
# • 1,000만 개의 난수를 생성한 후, 각 숫자가 소수인지 판별하는
#   작업을 단일 프로세스와 멀티 프로세스로 나누어 처리 시간을 비교
# • 요구사항
#  ‣ random을 사용하여 1,000만 개의 1~100,000 사이 정수 리스트를 생성하세요.
#  ‣ 숫자가 소수인지 판별하는 함수를 구현하세요.
#  ‣ 아래 두 가지 방식으로 소수의 개수를 세고 처리 시간을 비교하세요.
#    (a) 단일 프로세스 방식
#    (b) multiprocessing.Pool 사용 (병렬 처리)
#  ‣ 처리 시간과 소수 개수를 출력하세요.
#----------------------------------------------------------------------------

from multiprocessing import Pool
import random
import time
import math

list_rand= [random.randint(1,100000) for _ in  range(10_000_000)]


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    r = int(math.isqrt(n))
    for d in range(3, r + 1, 2):
        if n % d == 0:
            return False
    return True

def counting(lst):
    count = 0
    for x in lst:
        if is_prime(x):
            count += 1
    return count

def chunks(lst, k):
    n = len(lst)
    s = (n + k - 1) // k # n/k를 올림(ceiling) 해서 정수로 만들어 chunk 4개로 쪼개기
    return [lst[i:i+s] for i in range(0, n, s)]


t0 = time.time()
base = counting(list_rand)
t1 = time.time()
print(f"[Single Processing] prime_counts={base}, elapsed={t1 - t0:.4f}s")


parts = chunks(list_rand, 4)

t0 = time.time()
with Pool() as pool:
    # pool.map(counting, list_rand) 으로 정수 1000만개의 리스트를 직접 넣었더니 
    # counting(lst) 안에서 for x in '정수' 가 되어버려서 반복(iteration)이 안 되니까 TypeError('int is not iterable') 발생
    # 따라서 chunk로 쪼개서 parts = [chunk1, chunk2, chunk3, chunk4] 처럼 list 형태로 만들면 해결됨.
    result = pool.map(counting, parts) 
mp = sum(result)
t1 = time.time()

print(f"[Multi processing-4] prime_counts={mp}, elapsed={t1 - t0:.4f}s")