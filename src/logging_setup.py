import logging
import os

# 환경변수 LOG_LEVEL을 읽어서 로그 출력 기준을 정하고, 
# 로그 출력 형식(시간/레벨/이름/메시지)을 설정한 뒤, ml-service라는 이름의 로거를 꺼내주는 함수
# logging 모듈안에는 getLoger, basicConfig 등의 함수가 있다. 

def setup_logging() -> logging.Logger:
    # 환경변수에 LOG_LEVEL이 있다면 사용하고 없다면 INFO로 레벨을 설정
    # 환경변수 설정의 외부에서 별도의 파일 안에 사용자가 지정
    # os는 모듈, getenv는 그 안의 함수
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # basicConfig는 로그를 어떻게 출력할지 기본 설정을 하는 함수
    logging.basicConfig(
        level = level,
        # 각각 시간, 레벨이름, 로거이름, 실제 메시지
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    # Logger는 로그를 찍는 주체(도구), 이 함수의 뜻은 이름을 기준으로 Logger를 꺼내거나 새로 만든다.
    return logging.getLogger("ml-service")

