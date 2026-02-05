from pathlib import Path
import joblib
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "model.pkl"

# 모델파일이 없어서 에러가 생길 경우를 대비
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}. Run 'python src/train.py' first."
        )
    return joblib.load(MODEL_PATH)

_model = joblib.load(MODEL_PATH)

def predict(features):
    x = np.array(features, dtype=float).reshape(1,-1)
    return int(_model.predict(x)[0])