#---------------------------------------------------------------------------
# 작성자: 3002 기동주
# 작성 목적: [파이썬 1일차 실습 - 제너레이터 기반 메모리 절약형 로직 작성]
# 작성일: 2026.01.22
#
# 변경사항 내역(날짜, 변경목적, 변경내용 순으로 기입)
#---------------------------------------------------------------------------

# 1. 100만 개의 숫자 리스트를 처리하는 프로그램
#	 일반 리스트 방식은 메모리 과부하 발생 가능
#	 이를 해결하기 위해 제너레이터 기반 반복 구조를 직접 구현
#
#    1) 0부터 999,999까지의 정수를 담는 리스트를 생성하고 총합 구하기.
#    2) 같은 결과를 제너레이터 함수로 구현.
#    3) 두 방법의 메모리 사용 차이를 sys.getsizeof()로 확인.

import sys

N = 1000000

# 일반 리스트
list_comp = [x for x in range(1000000)]
list_sum = sum(list_comp)
# 제너레이터
gen = (x for x in range(N))
gen_sum = sum(gen)

list_size = sys.getsizeof(list_comp)
gen_size = sys.getsizeof(gen)

print("list memory: ", list_size, "bytes", "| sum:", list_sum)
print("generator memory:", gen_size, "bytes", "| sum:", gen_sum)
