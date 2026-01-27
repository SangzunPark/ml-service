## ML Service (day1)

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