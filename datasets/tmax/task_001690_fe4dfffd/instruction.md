You are an MLOps engineer tasked with deploying an experiment tracking and model serving pipeline for system telemetry data. We use a multi-service architecture where Redis acts as our artifact metadata tracker, and a Python web service serves the models.

Currently, an automated script runs Redis on `127.0.0.1:6379`.

You have a dataset of raw telemetry at `/home/user/telemetry.csv` containing the following columns: `cpu_usage`, `memory_mb`, `disk_io`, `network_rx`, `latency`, `is_anomaly`.

Your objective is to complete the following multi-stage workflow:

1. **Data Preprocessing & Model Training**
   Write a Python script (e.g., `train.py`) to load `/home/user/telemetry.csv` and train two models using `scikit-learn`.
   *Features:* `cpu_usage`, `memory_mb`, `disk_io`, `network_rx`.
   *Targets:* `latency` (Regression) and `is_anomaly` (Classification).
   *Data Cleaning:* 
   - `memory_mb` has missing values. Impute missing values with the median of the `memory_mb` column from the training set.
   - `disk_io` has extreme outliers. Clip any `disk_io` values strictly greater than `1000.0` to exactly `1000.0`.
   *Modeling:*
   - Train a `Ridge` regression model for `latency`.
   - Train a `LogisticRegression` model for `is_anomaly`.
   *Artifact Tracking:*
   - Save your trained models and the computed `memory_mb` median as a dictionary into a single file at `/home/user/artifacts/pipeline.joblib`. Create the directory if it doesn't exist.
   - Write a JSON string to the Redis instance on `127.0.0.1:6379` under the key `model:latest`. The JSON must exactly match this structure: `{"status": "trained", "path": "/home/user/artifacts/pipeline.joblib", "imputed_memory": <float_value_of_median>}`.

2. **Model Serving Service**
   Create and start a web service (using Flask, FastAPI, or similar) listening on `127.0.0.1:8000`.
   - It must expose a `POST` endpoint at `/predict`.
   - **Data Schema Enforcement:** The endpoint must accept JSON payloads and enforce the following schema rules:
     - `cpu_usage`: float, must be between 0.0 and 100.0 inclusive.
     - `memory_mb`: integer, must be strictly greater than 0. Optional (if missing, use the median computed during training).
     - `disk_io`: float, required.
     - `network_rx`: float, optional (defaults to `0.0` if not provided).
   - If the payload violates these schema rules, the service must return an HTTP `422 Unprocessable Entity` or `400 Bad Request` status code.
   - If valid, the service must apply the same `disk_io` outlier clipping (>1000.0 -> 1000.0) and predict using the loaded models.
   - The endpoint should return a JSON response: `{"latency_pred": <float>, "anomaly_pred": <int>}`.

Leave the web service running in the background so it can be verified. Use `/home/user/telemetry.csv` to build your pipeline.