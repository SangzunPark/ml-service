from pathlib import Path
import os

# jolib 이란 큰 numpy 배열을 포함한 객체를 저장하고 불러올 때 pickle 보다 훨씬 빠르고 효율적인 라이브러리
import joblib
import numpy as np
# boto3는 파이썬에서 AWS 서비스를 조작하는 공식 라이브러리. download_file  한 줄로 클라우드에 있는 모델을 서버로 가져옴
import boto3

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "model.pkl"

S3_BUCKET = os.getenv("MODEL_S3_BUCKET")
S3_KEY = os.getenv("MODEL_S3_KEY", "models/model.pkl")

# 앞에 _ 표시는 이것은 내부적으로 관리할 것이며 밖에서는 신경 쓰지 말고 공개된 함수들(_가 없는)만 사용해 라는 표시
# S3에서 모델 다운로드
def _download_model_from_s3():
    if not S3_BUCKET:
        raise RuntimeError(
            "MODEL_S3_BUCKET is not set. "
            "set env vars MODEL_S3_BUCKET and MODEL_S3_KEY (optional)."
        )
    
    MODEL_PATH.parent.mkdir(parents=True, exist_ok = True)

    s3 = boto3.client("s3")
    # 버킷은 S3 버킷 이름, 키는 그 안의 파일의 전체 경로 ex) models/v1/model.pkl
    s3.download_file(S3_BUCKET, S3_KEY, str(MODEL_PATH))


def load_model():
    if not MODEL_PATH.exists():
        _download_model_from_s3()
    return joblib.load(MODEL_PATH)

_model = load_model()

def predict(features):
    x = np.array(features, dtype=float).reshape(1, -1)
    return int(_model.predict(x)[0])