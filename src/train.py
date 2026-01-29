from pathlib import Path
import joblib
import numpy as np

# from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def main():
    root = Path(__file__).resolve().parents[1]

    X = np.load(root / "data" / "features" / "X.npy")
    y = np.load(root / "data" / "features" / "y.npy")

    # stratify =y 정상과 스팸의 비율을 원본과 동일하게 유지
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=2000)),
    ])

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print("Accuracy", accuracy_score(y_test, preds))

 

    model_dir = root / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    # models 폴더가 없는 CI 문제를 해결하기 위해 parents =True 는 상위 폴더가 없으면 전부 만들라는 뜻
    # exist_ok=Ture 는 이미 폴더가 있다면 그냥 사용    
    model_path = model_dir / "model.pkl"
    joblib.dump(model, model_path)


    print("Model saved to:", model_path)

if __name__ == "__main__":
    main()
