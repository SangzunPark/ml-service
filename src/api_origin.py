import time
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

from src.predict import predict


app = FastAPI(title="ML Service", version="0.2.0")

logging.basicConfig(level=logging.INFO)
# INFO 이상 레빌의 로그만 출력하겠다 Debug / INFO / WARNING / ERROR / CRITICAL
logger = logging.getLogger("ml-service")
# 로그를 찍는 주체를 선언

class PredictRequest(BaseModel):
    features: List[float] = Field(..., description="Length-30 feature vector")


class PredictResponse(BaseModel):
    prediction: int
# 위의 class가 함수가 아닌 이유는 행동이 아닌 모양검증이기 때문이고 pydantic의 BaseModel이 이것을 수행하며 이것이 FastAPI의 장점
# 만약 def로 하려고 하면 검증 코드를 모두 작성해야 하기 때문에 FastAPI의 장점이 모두 사라짐


@app.get("/health")
def health():
    return {"status": "ok"}
# URL로 부터 "/요청" 이 들어오면 이 함수를 실행하라
# @은 파이썬의 데코레이터로, 아래에 정의된 함수를 약간 변형하거나 등록해라 라는 의미
# health 함수를 FastAPI 서버에 /health 경로의 GET 요청 처리기로 등록
# 메서드 GET은 조회이며 상태확인, 데이터 조회에 사용
# 메서드 POST 는 생성/계산이며, 예측요청 데이터 제출에 사용
# 엔드포인트는 외부에서 이 기능을 쓰려면 여기로 요청해라 라고 정해놓은 주소 /health, /docs, /predict 등
# HTTP 매서드 와 경로(path)가 한세트 ex: GET /health
# 다른 말로는 요청(request) 가 도착해서 실제 로직이 실행되는 끝 지점

@app.post("/predict", response_model=PredictResponse)
# response_model은 FastAPI에게 응답형식선언, 자동검증, 자동문서화(/docs), 보안 등의 역할을 한다. 
def do_predict(req: PredictRequest):
    # 파이썬 자체 문법으로 req는 변수이름, 뒷부분은 type hint
    # type hint란 이 변수는 이런 타입이 들어올 것이다라고 선언
    start = time.time()
    try:
        if len(req.features) != 30:
            raise ValueError("features must have length 30")
        yhat = predict(req.features)
        # req는 요청이 들어올 때 FastAPI가 자동으로 생성하는 객체다

        # 처리시간 계산
        elapsed_ms = (time.time() - start) * 1000
        # 성공 로그, 소수 2째 자리까지 / 로깅 전용 문자열 포맷, %는 값이 들어올 자리
        # logger.info("...", 값)
        logger.info("predict ok | latency_ms=%.2f", elapsed_ms)

        return {"prediction": yhat}
    except Exception as e:
        # 실패로그
        logger.error("predict failed | error=%s", str(e))
        raise HTTPException(status_code=400, detail=str(e))
                            
