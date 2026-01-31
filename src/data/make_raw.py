from sklearn.datasets import load_breast_cancer
from src.config import load_config, project_root

# 메모리 안에 있던 raw를 파일로 고정하고 경로를 config.yml이 통제하도록 하는 과정

def main():
    cfg = load_config()
    root = project_root()

    out_path = root / cfg["data"]["raw_path"]

    # 여기서 사용하는 데이터는 Bunch 객체라고 한다. 딕셔너리처럼 여러 값이 있고 data["frame"] 처럼 접근가능하고
    # data.frame 처럼 점 (.)으로도 접근 가능하다
    # as_frame=Ture 는 같은 데이터를 Numpy 배열로 받을지, pandas DataFrame으로 받을 지 정하는 스위치이며
    # 단순 X,y 어레이인 Numpy 배열고 달리 DataFrame은 features(df)와 target(series)가 합쳐진 형태 이며
    # features 이름, target class 이름 그리고 데이터셋 설명 텍스트를 포함한다(data.DESCR)
    data = load_breast_cancer(as_frame=True)
    # data.frame은 target 값까지 모두 포함해서 보겠다는 의미 반대로 data.data 는 features 값만 있는 데이터프레임
    # X = data.data / y= data.target (data.target_names)
    df = data.frame

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

    print(f"Saved raw data to {out_path}")

if __name__ =="__main__":
    main()

