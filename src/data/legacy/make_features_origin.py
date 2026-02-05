from pathlib import Path
import numpy as np
import pandas as pd

# 모델 전용 입력

def main():
    root = Path(__file__).resolve().parents[2]
    proc_path = root / "data" / "processed" / "breast_cancer_processed.csv"

    df = pd.read_csv(proc_path)

    X = df.drop(columns=['target']).values
    y = df["target"].values

    feat_dir = root / "data" / "features"
    feat_dir.mkdir(parents=True, exist_ok=True)
    # npy는 numpy에서 사용하는 바이너리 데이터 저장 형식으로 텍스트 형식인 csv나 txt보다 읽기/쓰기 속도가 빠르며 용량도 저렴
    np.save(feat_dir / "X.npy", X)
    np.save(feat_dir / "y.npy", y)

    print("Saved features to data/features/")

if __name__=="__main__":
    main()