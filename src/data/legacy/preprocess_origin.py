from pathlib import Path
import pandas as pd

def main():
    root = Path(__file__).resolve().parents[2]
    raw_path = root / "data" / "raw" / "breast_cancer_raw.csv"
    out_path = root / "data" / "processed" / "breast_cancer_processed.csv"

    df = pd.read_csv(raw_path)

    # 이 데이터에서는 이러한 전처리가 큰 의미는 없지만 구조를 만드는 것이 목적
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

    print(f"Saved processed data to {out_path}")


if __name__ == "__main__":
    main()