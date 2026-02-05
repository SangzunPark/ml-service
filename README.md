# ML Service — End-to-End ML API with Docker & AWS

## Overview
This project demonstrates how a trained Machine Learning model can be transformed into a **reproducible, deployable service**.

Instead of focusing on model performance tuning, the goal is to:
- manage ML artifacts reproducibly,
- expose predictions via an API,
- and run the same service consistently across **local, CI, and cloud environments**.

---

## Problem Statement
Machine Learning models are often developed as notebooks or scripts that are hard to reuse, deploy, or operate reliably.

This project addresses the following problems:
- ML models tightly coupled to local environments
- Lack of reproducible data and training pipelines
- Difficulty serving models as stable APIs
- Environment mismatch between local, CI, and production

**Goal:**  
Build a minimal yet realistic ML service that bridges the gap between experimentation and production.

---

## System Architecture & Flow

```
[ Raw Data ]
     |
     v
[ make_raw.py ]
     |
     v
[ preprocess.py ]
     |
     v
[ make_features.py ]
     |
     v
[ train.py ]
     |
     v
[ model.pkl ]
     |
     v
[ FastAPI (/predict) ]
     |
     v
[ Docker Container ]
     |
     v
[ Local / CI / AWS EC2&S3 ]
```

---

## Project Structure

```
ml-service/
├── src/
│   ├── api.py
│   ├── train.py
│   ├── predict.py
│   ├── config.py
│   └── data/
│       ├── make_raw.py
│       ├── preprocess.py
│       └── make_features.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── features/
├── models/
│   └── model.pkl
├── tests/
├── config.yml
├── Dockerfile
└── README.md
```

---

## Data Pipeline

The data pipeline is explicitly split into stages to ensure **reproducibility and re-executability**.

```
raw → processed → features → model
```

### Execution Order
```bash
python -m src.data.make_raw
python -m src.data.preprocess
python -m src.data.make_features
python -m src.train
```

Each step:
- has clear inputs and outputs,
- can be rerun independently,
- does not mutate upstream artifacts.

---

## Configuration

All paths and model metadata are centralized in a YAML configuration file.

```yaml
data:
  raw_path: data/raw/breast_cancer_raw.csv
  processed_path: data/processed/breast_cancer_processed.csv
  features_dir: data/features

model:
  path: models/model.pkl
  version: "0.6.0"
```

The configuration is loaded via `src/config.py`, allowing:
- environment-independent path resolution,
- easy changes without modifying code.

---

## Training

```bash
python -m src.train
```

- Trains a scikit-learn model
- Saves the trained artifact as `models/model.pkl`
- Training and inference logic are strictly separated

---

## API Service

### Run API locally
```bash
uvicorn src.api:app --reload
```

### Endpoints
- `GET /health` — service health & model version
- `POST /predict` — model inference

Example response:
```json
{
  "prediction": 1,
  "model_version": "0.6.0"
}
```

---

## Logging

- Centralized logging configuration
- Configurable log level via environment variable

```bash
LOG_LEVEL=INFO
LOG_LEVEL=DEBUG
```

Logged information includes:
- request success/failure
- inference latency (ms)
- stack traces on errors

---

## Tests

```bash
pytest -q
```

Tests validate:
- API availability
- response schema
- prediction behavior

Tests are executed automatically in CI to prevent regressions.

---

## Docker

### Build
```bash
docker build -t ml-service:0.6.0 .
```

### Run
```bash
docker run -p 8000:8000 ml-service:0.6.0
```

The same Docker image is used across:
- local development
- CI validation
- AWS EC2 deployment

---

## Design Decisions & Trade-offs

### Why FastAPI?
- Automatic request validation (Pydantic)
- Auto-generated API documentation
- Well-suited for ML inference services

### Why Docker?
- Eliminates environment inconsistencies
- Ensures reproducibility across machines
- Simplifies deployment to cloud environments

### Why script-based data pipeline?
- Workflow orchestration tools (Airflow, Prefect) would be overkill
- Focus is on **pipeline structure**, not scheduling

---

## Limitations

- No autoscaling or high-availability setup
- No automated retraining pipeline
- Model performance optimization is out of scope
- Security (auth, rate limiting) not implemented

These limitations are intentional to keep the project focused on **ML service architecture fundamentals**.

---

## What I Learned

- How to transition from ML experimentation to a deployable service
- How to design reproducible data and training pipelines
- How Docker enables consistent execution across environments
- How operational concerns (logging, config, versioning) impact ML systems

---

## Status

-  Local execution
-  CI validation
-  Dockerized service
-  AWS EC2 deployment

---

### Final Summary
> *“I built an end-to-end ML service that is reproducible, containerized, and deployable across local, CI, and cloud environments.”*
