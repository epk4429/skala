#---------------------------------------------------------------------------
# 작성자: 3002 기동주
# 작성 목적: [파이썬 1일차 실습 -.env + logging 활용 스크립트 환경 구성]
# 작성일: 2026.01.22
#
# 변경사항 내역(날짜, 변경목적, 변경내용 순으로 기입)
#---------------------------------------------------------------------------
# •     .env 파일을 사용하여 다음 값을 저장
#        ‣     LOG_LEVEL=DEBUG
#        ‣     APP_NAME=MyCoolApp
# •     Python 코드에서 python-dotenv를 이용해 .env 파일의 값을 로딩하고, logging 모듈을 통해 로그 설정을 아래와 같이 구성
#        ‣     로그 파일명: app.log
#       ‣     로그 레벨: .env에서 가져온 값 (DEBUG, INFO 등)
#       ‣     로그 포맷: 시간 | 로그레벨 | 메시지
#       ‣     로그 출력: 콘솔 + 파일 모두
# •     다음 메시지를 로그로 출력
#       ‣     [INFO] 앱 실행 시작
#       ‣     [DEBUG] 환경 변수 로딩 완료
#       ‣     [ERROR] 예외 발생 예시
# •     실습 폴더 구조 예시
#  env_logging_example/
#        │
#        ├── .env
#        ├── main.py
#        └── app.log ← 실행 후 생성됨
# 1단계 – .env 작성
#       ·        .env 파일을 만들고 다음 키-값을 저장
#             LOG_LEVEL=???
#             APP_NAME=???
#       ·        LOG_LEVEL에는 DEBUG 또는 INFO,
#       ·        APP_NAME에는 자유로운 앱 이름 입력
# 2단계 – 환경 변수 로드
#       ·        python-dotenv 모듈 설치
#             pip install python-dotenv
#       ·        .env 파일을 읽어오는 코드 작성 (힌트: load_dotenv() 사용)
#       ·        os.getenv("LOG_LEVEL") 로 변수 읽기
# 3단계 – logging 설정
#       ·        로그 파일명: app.log
#       ·        로그 포맷: 시간 [레벨] 메시지
#       ·        로그 레벨: .env에서 가져온 값 사용 (getattr(logging, log_level))
#       ·        콘솔 + 파일 동시에 출력되도록 핸들러 구성
# 4단계 – 로그 출력 테스트
#       ·        INFO 레벨 메시지: "앱 실행 시작"
#       ·        DEBUG 레벨 메시지: "환경 변수 로딩 완료"
#       ·        ERROR 레벨 메시지: ZeroDivisionError 예외 발생 시 출력
# 5단계 – 실행 후 확인
#       ·        콘솔 화면 출력 확인
#       ·        app.log 파일 내용 확인
#--------------------------------------------------------------------------------
import os
from dotenv import load_dotenv
import logging
from logging.handlers import TimedRotatingFileHandler

# 현재 작업 디렉토리(보통 실행 위치) 기준으로 .env 파일을 찾아서, 그 안의 KEY=VALUE들을 프로세스 환경변수(os.environ) 로 로딩해줍니다.
# 그래서 아래 os.getenv()에서 .env에 있는 값을 읽을 수 있게 됩니다.
load_dotenv() 

# 환경변수 APP_NAME 값을 가져옵니다. 있으면: 그 값 사용, 없으면: 기본값 "MyCoolApp" 사용
APP_NAME = os.getenv("APP_NAME", "MyCoolApp")

# 환경변수 LOG_LEVEL 문자열을 가져오고(없으면 "INFO")
LOG_LEVEL_STR = os.getenv("LOG_LEVEL", "INFO").upper()

# logging 모듈 안에서 LOG_LEVEL_STR라는 이름의 속성을 찾아 가져옵니다. 즉, 문자열("DEBUG") → 실제 로깅 레벨 상수(logging.DEBUG) 로 바꾸는 변환기입니다.
# 예: LOG_LEVEL_STR="DEBUG"면 logging.DEBUG(숫자 레벨 값)를 가져옴
# 만약 "DEBIG"처럼 오타면 없으니까 기본값 logging.INFO로 대체
LOG_LEVEL = getattr(logging, LOG_LEVEL_STR, logging.INFO)

# 로거 생성 및 레벨
# 이름이 APP_NAME인 로거 객체(Logger) 를 가져옵니다. 로거는 로그를 받는 창구
# 로거(Logger)가 하는 일 3가지
# 1. 로그를 받는다: logger.info(...), logger.debug(...), logger.error(...) 같은 호출을 받는 주체가 Logger
# 2. 필터링한다 (레벨 컷): logger.setLevel(INFO)면 DEBUG 같은 낮은 레벨은 아예 처리 안 하고 버립니다.
# 3. 핸들러에게 뿌린다: logger.addHandler(console_handler), logger.addHandler(file_handler) 
#                    이렇게 붙어있는 핸들러들에게 “이 로그 건을 처리해라” 하고 넘깁니다.
logger = logging.getLogger(APP_NAME)

# 이 로거가 처리할 최소 레벨을 정합니다.예를 들어 INFO면: logger.debug()는 무시(기록 안 함), logger.info()/warning()/error()는 처리
logger.setLevel(LOG_LEVEL)

# 로그 포맷
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")


# 핸들러: 로그를 내보내는 목적지(콘솔, 파일 등)

# 기본적으로 sys.stderr 쪽(터미널/콘솔)에 로그를 출력하는 핸들러입니다. 여기서는 "콘솔 출력 담당" 입니다.
console_handler = logging.StreamHandler()
# 콘솔에는 어느 레벨부터 찍을지 를 결정합니다. 주의 포인트: 로깅은 보통 로거 레벨 + 핸들러 레벨 둘 다 통과해야 찍힙니다.
console_handler.setLevel(LOG_LEVEL)
# 콘솔로 나갈 때도 위에서 만든 포맷을 적용합니다.
console_handler.setFormatter(formatter)


# 파일 핸들러 (app.log 파일 출력)

# 로그를 파일로 저장하는 핸들러입니다.
file_handler = logging.FileHandler("app.log", encoding="utf-8")
# 파일에는 어느 레벨부터 기록할지 결정합니다.
file_handler.setLevel(LOG_LEVEL)
# 파일 로그에도 같은 포맷 적용.
file_handler.setFormatter(formatter)

# 이 로거로 들어온 로그는 콘솔에도 보내고, 파일에도 보내라
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# INFO 레벨 로그 발행
logger.info("앱 실행 시작")
# DEBUG 레벨 로그 발행, 만약 .env의 LOG_LEVEL=INFO면 이 줄은 안 찍힙니다(DEBUG는 INFO보다 낮아서)
logger.debug("환경 변수 로딩 완료")
try:
    _ = 1 / 0
except ZeroDivisionError:
    logger.error(" ZeroDivisionError 예외 발생 시 출력")


