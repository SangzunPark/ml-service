## ML Service

### Setup
pip install -r requirements.txt

### Train
python src/train.py

### Predict
python src/test_predict.py

### Run API
uvicorn src.api:app --reload

### Tests
pytest -q

## Docker

### Build
docker build -t ml-service

### Run
docker run -p 8000:8000 ml-service

## Data Pipeline

raw -> processed -> features -> model

## Steps
1. python src/data/make_raw.py
2. python src/data/preprocess.py
3. python src/data/make_features.py
4. python src/train.py