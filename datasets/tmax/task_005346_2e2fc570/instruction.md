You are tasked with building and deploying a real-time feature engineering and data cleaning service. Our team is transitioning from static notebook analyses to a microservice architecture. 

Currently, we have two services running locally on your system:
1. **PostgreSQL** (`127.0.0.1:5432`): Contains a database named `telemetry` with a table `raw_signals`. The table has an `id` column, a `target` column, and 20 continuous numerical feature columns (`f1` to `f20`). There are missing values in some columns.
2. **Redis** (`127.0.0.1:6379`): Used for caching the processed datasets.

Your job is to create a Python web service (using FastAPI, Flask, or any standard HTTP framework) that connects these components, performs statistical analysis, and serves the cleaned data.

**Service Requirements:**
- The service must bind to `127.0.0.1:8080`.
- Every endpoint must require an authorization header: `X-API-Token: token_ds_7788`.
- Implement the following endpoints:

1. `POST /engineer_features`:
   - Connects to the PostgreSQL `telemetry` database (user: `admin`, password: `password123`).
   - Fetches the `raw_signals` table.
   - Performs a correlation and covariance analysis to identify redundant features. Specifically, drop any feature that has a Pearson correlation > 0.90 with another feature (keep the one with the lower index, e.g., if f3 and f5 are correlated, drop f5).
   - Fills missing values in the remaining features using the mean of each respective column.
   - Performs a 3-fold cross-validation Ridge Regression (alpha=1.0) predicting the `target` column to compute feature importances (absolute value of coefficients).
   - Selects the top 5 most important features.
   - Saves the final list of the 5 selected feature names as a JSON array to `/home/user/selected_features.json`.
   - Serializes the cleaned dataset (only the `id`, `target`, and the 5 selected features) and stores it in Redis under the key `dataset:cleaned` as a JSON string (list of dictionaries).
   - Returns a 200 OK status with a JSON body `{"status": "engineered"}`.

2. `GET /fetch_cleaned`:
   - Retrieves the cached dataset from Redis key `dataset:cleaned`.
   - Returns the dataset as a JSON response (status 200).

**Analysis Environment Setup:**
You will need to install your own dependencies in `/home/user` (e.g., `pip install pandas scikit-learn psycopg2-binary redis flask`). Ensure the application is actively running and listening on port 8080 in the background or foreground before you complete the task, as an automated verifier will issue real HTTP requests to your endpoints to test the end-to-end flow.