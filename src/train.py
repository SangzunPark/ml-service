from pathlib import Path
import joblib

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def main():
    data = load_breast_cancer()
    X, y = data.data, data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline([
        ("scalar", StandardScaler()),
        ("clf", LogisticRegression(max_iter=2000)),
    ])

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print("Accuracy", accuracy_score(y_test, preds))

    root = Path(__file__).resolve().parents[1]

    model_dir = root / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    # models 폴더가 없는 CI 문제를 해결하기 위해     
    model_path = model_dir / "model.pkl"
    joblib.dump(model, model_path)


    print("Model saved to:", model_path)

if __name__ == "__main__":
    main()
