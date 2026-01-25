from sklearn.datasets import load_breast_cancer
from predict import predict

data = load_breast_cancer()
sample = data.data[0].tolist()

print("Prediction:", predict(sample))
