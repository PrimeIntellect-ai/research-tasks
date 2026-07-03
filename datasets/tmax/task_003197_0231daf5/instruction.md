You are an ML Engineer preparing a data preprocessing and serving pipeline. We need to ingest raw dataset, apply dimensionality reduction, and serve the transformed features via a REST API for upstream modeling services.

There are three main parts to this task:

1. **Fix the Vendored Package:**
   We are using a proprietary internal package for serving ML features, located at `/app/feature_server_pkg-1.2.0`. However, the package is currently broken. The `Makefile` used to build and install it locally has a typo in the Python build command, and it hardcodes an incorrect Python version. You must fix the `Makefile` and successfully install the package into the local environment (`pip install .` or via the fixed `make install`).

2. **Build the ETL and Dimensionality Reduction Pipeline:**
   Write a reproducible Python script at `/home/user/etl_pipeline.py`. 
   The script must:
   - Read a CSV file located at `/app/data/raw_features.csv` (contains 50 numeric columns: `f_0` to `f_49`).
   - Standardize the features (mean = 0, variance = 1).
   - Apply Principal Component Analysis (PCA) to reduce the dimensionality to exactly 5 components.
   - Save the PCA model using `joblib` or `pickle` to `/home/user/pca_model.pkl`.
   - Save the transformed data to `/home/user/processed_features.csv` (columns should be named `pc_1`, `pc_2`, `pc_3`, `pc_4`, `pc_5`).

3. **Serve the Data via HTTP:**
   Using the fixed `feature_server_pkg` (which wraps standard Python HTTP server functionalities) or standard frameworks like FastAPI/Flask (if the wrapper imports them), create a service script at `/home/user/serve_features.py` that listens on `127.0.0.1:8080`.
   The service must implement the following protocol:
   - **GET /health**: Returns `{"status": "ok"}`
   - **POST /transform**: Accepts a JSON payload `{"features": [list of 50 floats]}`. It must load the saved scaler and PCA model, apply the exact same transformation to this new data point, and return `{"reduced_features": [list of 5 floats]}`.
   - The API must require an Authorization header: `Bearer secret_ml_token_99X`. If missing or incorrect, return a 401 Unauthorized status.

Start the service in the background and ensure it is listening on port 8080 before completing the task. Create a log file at `/home/user/server.log` capturing the standard output and error of the server process.