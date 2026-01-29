#---------------------------------------------------------------------------
# 작성자: 3002 기동주
# 작성 목적: [파이썬 2일차 실습 - 데코레이터로 함수 실행시간 측정기 구현]
#           데코레이터 문법의 구조 이해 (*args, **kwargs, 함수 중첩 등)
#           time 모듈을 활용한 실행시간 측정 로직 구현
#           실제 함수에 데코레이터 적용 및 시간 측정 확인
# 작성일: 2026.01.26
#
# 변경사항 내역(날짜, 변경목적, 변경내용 순으로 기입)
#----------------------------------------------------------------------------
#
# • measure_time이라는 이름의 데코레이터 함수를 작성
# • 이 데코레이터는 어떤 함수든 wrapping후 실행 시간을 측정한 뒤,
#   ‣     함수 실행 결과는 그대로 반환하고
#   ‣     실행 시간은 "함수명 took 0.1234 seconds"와 같이 출력
# • 임의의 연산 지연이 있는 함수 slow_function()에 적용하여 정상 동작을 확인
#----------------------------------------------------------------------------
import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@measure_time
def hello():
    print("Hello Python!")

@measure_time
def slow_function():
    time.sleep(3)
    print(f"slept {3} seconds")

hello()
slow_function()