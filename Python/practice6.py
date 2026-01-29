#---------------------------------------------------------------------------
# 작성자: 3002 기동주
# 작성 목적: [파이썬 2일차 실습 - typing, mypy, 그리고 성능 측정 비교 ]
#           Python의 타입 힌트(typing)를 이해하고 코드에 적용
#           정적 타입 검사 도구인 mypy를 사용하여 코드의 안정성을 확인
#           타입 힌트 유무에 따라 코드 실행 성능에 차이가 있는지 timeit으로 비교
# 작성일: 2026.01.26
#
# 변경사항 내역(날짜, 변경목적, 변경내용 순으로 기입)
#---------------------------------------------------------------------------
# • 다음 요구 사항에 맞춰서 코드를 작성하고 결과를 비교
# • 두 가지 버전의 함수를 작성
#   ‣ A 버전 : 타입 힌트를 사용하지 않은 함수
#   ‣ B 버전 : 타입 힌트를 적용한 함수
# • 두 버전 모두 동일한 작업을 수행
#   ‣ 입력 : 정수 리스트 → 출력 : 각 원소의 제곱을 더한 합
# • mypy를 이용해 버전 B의 타입을 검사해보고, 결과를 확인
# • timeit을 사용하여 두 버전의 실행 성능을 각각 측정하고 성능 차이를 비교
#----------------------------------------------------------------------------

from typing import List
import timeit


def ver_A(num):
    return sum(x**2 for x in num)

def ver_B(num:List[int])->int:
    return sum(x**2 for x in num)


if __name__ == "__main__":
    
    list_int = list(range(100000))


    time_a = timeit.timeit("ver_A(list_int)", number = 100, globals=globals())
    time_b = timeit.timeit("ver_B(list_int)", number = 100, globals=globals())

    # 런타임에 영향을 거의 주지 않는다. 
    print(f"A(no type hints) elapsed : {time_a:.6f}s")
    print(f"B(   type hints) elapsed: {time_b:.6f}s")

    # ver_B([1, 2, "3"])  # <- 주석 풀고 문자열 섞은 list를 넣으면 mypy가 잡아줌