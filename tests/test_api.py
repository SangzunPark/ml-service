from fastapi.testclient import TestClient
from src.api import app
from sklearn.datasets import load_breast_cancer
#TestClient 는 HTTP를 흉내내서 메모리 안에서 테스트하는 테스트용 클라이언트
# uvicorn 보다 빠르고 안정적이며 무엇보다 CI에서 가능
# pytest는 테스트를 실행, 관리하며 testclient는 API 요청을 모방한다
# pytest 실행하기전에 pip install httpx

client = TestClient(app)

def test_health_ok():
    r = client.get("/health")
    # assert는 이것이 참인지 확인하라
    assert r.status_code ==200

    body = r.json()
    assert body["status"] == "ok"
    # r.json 이란 응답 body(JSON)를 Python 자료구조로 바꿔준다는 의미 서버의 응답예시는 {"prediction": 1}

    assert "model_Version" in body
    # isinstance(x,str) 은 x가 str타입인지 확인해 주는 함수
    assert isinstance(body["model_version"], str)
    # 모델버전값이 빈 문자열이 아니어야 한다는 뜻 True 면 통과
    assert body["model_version"] != ""
    

def test_predict_ok():
    data = load_breast_cancer()
    sample = data.data[0].tolist()
    #첫 번째 샘플의 features 30, numpy 배열은 JSON으로 보내기 애매해 일반 파이썬 리스트로 변환
    # json array 의 형태는 [1.2.3] 으로 파이썬 list 형태와 형태가 같음
    # 참고로 json object 형태는 key:value 형태로 파이썬의 dict와 동일

    r = client.post("/predict", json={"features":sample})
    assert r.status_code == 200

    body = r.json()
    assert body()["prediction"] in [0, 1]

    assert "model_Version" in body
    assert isinstance(body["model_version"], str)
    assert body["model_version"] != ""

