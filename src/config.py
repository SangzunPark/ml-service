# 프로젝트 전반에서 설정과 프로젝트 루트 경로를 하나의 표준 방식으로 제공하기 위한 유틸리티 모듈

# Path OS 독립적인 경로 처리, 윈도우 리눅스 공통, Path는 경로는 문자열이 아닌 객체로 다루게 해주는데
# 우선 OS바다 경로 표기가 다르고 각 지점이 객체이기 때문에 검색, 활용이 수월하다
from pathlib import Path
# 환경변수(environment variable) 프로그램이 실행될때 코드 바깥에서 건네주는 설정 값
# CONFIG_PATH는 이 환경변수 이름이고 설정파일을 어디서 읽을지, 그 경로는 코드 밖에서 정해주는 것
import os
# config.yml은 파이썬에게는 단순한 텍스트 일 뿐인데 이것을 dict로 변환해야하며 그것을 하는 것이 yaml.safe_load()
import yaml

# 종합하면 설정 파일 경로를 밖에서 바꾸고 그 설정을 읽어서 dict로 만들어 코드에서 사용

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = ROOT / "config" / "config.yml"

# 여기서 화살표는 type hint 문법이며 이 함수는 실행되면 dict를 반환할 것으로 기대된다는 뜻. 실제 실행에 영향은 거의 없음
# 하지만 사람, IDE(VScode), 타입검사 도구에게 의미를 전달 하며 실무에서 큰 영향
def load_config() -> dict:
    # 해석하면, CONFIG_PATH라는 환경변수가 있다면 그 값을 쓰고 없다면 기본값(DEFAULT_CONFIG_PATH) 을 써라
    # 전통적으로 환경변수는 대문자+언더스코어 를 사용
    # os.getenv()는 문자열 이름표를 받는 함수 때문에 환경변수가 문자
    # 여기서 선언한 CONFIG_PATH는 나중에 터미널 등에서 설정해서 사용하기 위함. 현재는 특별한 값이 없음
    cfg_path = Path(os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH))
    # 파일읽기, 파싱 복습
    with open(cfg_path, "r", encoding="utf-8") as f:
        # 실무에서는 safe_load가 정석인데 이 설정은 데이터만 읽는다
        # 아래 코드에서 실질적으로 dict로 변환이 되는데(파싱) 이것은 원래 config,yml이 map 구조라서 이다.
        # 여기서 map 구조란 프로그램 전반에서 쓰는 일반 용어로 key/value 구조를 의미 즉 dict
        return yaml.safe_load(f)

# 이 코드의 목적은 실제 주소를 hidden 화 하며 의미를 이름으로 고정(이건 프로젝트 최상위 루트다)
# 확장성, 나중에 바꿀 여지를 남기고 테스트에서 교체하기 쉽다.
# 5주차의 주제가 "바뀔 수 있는 지점을 한곳에 모으는 것이기 때문"   
def project_root() -> Path:
    return ROOT