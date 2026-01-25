from pathlib import Path
import joblib
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "model.pkl"

_model = joblib.load(MODEL_PATH)

def predict(features):
    x = np.array(features, dtype=float).reshape(1,-1)
    return int(_model.predict(x)[0])