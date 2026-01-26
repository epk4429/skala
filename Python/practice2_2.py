#---------------------------------------------------------------------------
# 작성자: 3002 기동주
# 작성 목적: [파이썬 1일차 실습 - 제너레이터 기반 메모리 절약형 로직 작성]
# 작성일: 2026.01.22
#
# 변경사항 내역(날짜, 변경목적, 변경내용 순으로 기입)
#---------------------------------------------------------------------------

# 2. 아래 조건을 만족하는 제너레이터 함수 even_square_gen(n)을 작성
#	- 0 이상 n 미만의 정수 중 짝수만 제곱해서 하나씩 생성 (yield 활용)
#	
# 	해당 제너레이터를 이용해 0부터 1,000,000까지의 짝수의 제곱 총합을 계산
# 	이 때의 메모리 사용량과 처리 속도를 비교 (time 모듈 활용)

import time

# 짝수 제곱 반환 제너레이터
def even_square_gen(n):
    for i in range(n):
        if i % 2 == 0:
            yield i * i

# 제너레이터 실행 시간
gen_start = time.time()
gen_result = sum(even_square_gen(1000000))
gen_end = time.time()

# 리스트 짝수 제곱 및 실행 시간
list_comp = [i * i for i in range(1000000) if i % 2 == 0]

list_start = time.time()
list_result = sum(list_comp)
list_end = time.time()

# 실행 시간 비교
print("제너레이터 짝수 제곱 총합:", gen_result)
print("리스트 짝수 제곱 총합:    ", list_result)

print("제너레이터 실행 시간:", gen_end - gen_start)
print("리스트 실행 시간:    ", list_end - list_start)