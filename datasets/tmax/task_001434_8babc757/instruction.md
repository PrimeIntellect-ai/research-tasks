I need you to build a complete ETL and model-serving pipeline for a proprietary sensor system. 

We have a legacy, stripped compiled binary located at `/app/sensor_simulator` that generates raw sensor readings. Unfortunately, we lost the source code for it. When executed, it outputs a continuous stream of JSON lines to standard output. Some of these readings represent anomalous sensor spikes, but the raw data is noisy.

Your task is to:
1. Execute and analyze the output of `/app/sensor_simulator`.
2. Build an ETL pipeline in Python that collects a sufficient sample of this data and extracts relevant features.
3. Train an anomaly detection or binary classification model (using `scikit-learn` or similar) to identify anomalous readings. You'll need to figure out the underlying pattern of what constitutes an anomaly based on the data distribution (hint: look for combinations of extreme values in specific sensor channels).
4. Create a web service using Python (e.g., Flask or FastAPI) that serves this model.
5. The service must listen exactly on `127.0.0.1:8080`.
6. The service must expose a `POST /predict` endpoint. It will receive a JSON payload with a single sensor reading (matching the format output by the binary).
7. The endpoint must return a JSON response in the exact format: `{"anomaly": true}` or `{"anomaly": false}`.
8. Secure the endpoint: It must require a Bearer token for authentication. The token must be exactly `Bearer etl-pipeline-secret-2024`. Requests without this exact token should be rejected with a 401 Unauthorized status.

You must handle all package and dependency installations yourself using standard Python tools. Ensure the pipeline is reproducible. Leave the server running in the background or foreground so that my automated test suite can send requests to it.