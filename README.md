## ML Service

### Setup
pip install -r requirements.txt

### Train
python -m src.train

### Predict
python -m src.test_predict

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

## Steps (-m for package run)
1. python -m src.data.make_raw
2. python -m src.data.preprocess
3. python -m src.data.make_features
4. python -m src.train