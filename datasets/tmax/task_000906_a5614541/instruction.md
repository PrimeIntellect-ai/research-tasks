You are an AI data scientist assisting with a broken machine learning reporting pipeline. We have a locally deployed multi-service architecture under `/app/` that is supposed to process CSV files, run statistical validations, and serve the results. However, the data analyst is complaining that the system is producing "blank" or failed reports due to backend misconfigurations and some sloppy Pandas/Scikit-learn code.

The system is composed of:
1. **Redis**: Runs as a background service.
2. **Worker API** (Flask): Listens on port `5001`. It provides an endpoint `POST /process` which accepts a multipart form data containing a CSV file (`file` field).
3. **Report API** (FastAPI): Listens on port `5002`. It provides an endpoint `GET /report` which fetches the latest processed insights from Redis.

To test the services, a startup script `/app/start.sh` brings them up.

However, the pipeline is failing for multiple reasons:
1. **Glue & Configuration**: The services are failing to communicate. You need to inspect `/app/config.json` and the environment variables in `/app/start.sh` to fix the Redis connection parameters (port, host, and password). The Redis instance requires the password `stat-sec-99`, but the APIs are currently configured to connect without authentication or on the wrong port.
2. **Data Transformation & Reproducibility**: The code in `/app/worker.py` attempts to process the uploaded dataset, which contains numerical features, a string categorical column named `category`, and a numerical `target` column.
   You must fix `/app/worker.py` to:
   - One-hot encode the `category` column (do not drop any categories, use standard `pandas.get_dummies` or similar).
   - Compute the full Pearson correlation matrix across all features (excluding the `target`).
   - Train a Ridge regression model (`alpha=1.0`) to predict `target` using all other transformed features.
   - Run a 5-fold cross-validation (`KFold` with `shuffle=True`). To fix the pipeline reproducibility test failures, you must set `random_state=42` in the KFold splitter!
   - Save the exact mean $R^2$ score (`cv_score`) and the `correlation_matrix` (as a nested dictionary) to Redis.

Your job is to fix `/app/config.json`, `/app/start.sh`, and `/app/worker.py`. When you are finished, ensure all three services are running properly so that an external automated test can perform a `POST` request to `/process` with a test CSV and then successfully retrieve the insights via `GET /report`.