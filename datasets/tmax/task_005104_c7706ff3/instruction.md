You are a data scientist tasked with building a predictive API for server latency. You have a raw dataset of server metrics in `/home/user/data/server_metrics.csv`.

Your objectives:

1. **Data Cleaning & Feature Engineering:**
   - Load `/home/user/data/server_metrics.csv` (Columns: `cpu_usage`, `mem_usage`, `disk_io`, `network_in`, `latency`).
   - Impute any missing values in the `cpu_usage` column using the median of that column.
   - Remove any rows where `disk_io` is strictly greater than 1000 (these are extreme outliers).
   - Compute the Pearson correlation matrix of the cleaned dataset. Identify the TWO features (excluding `latency` itself) that have the highest absolute correlation with `latency`.

2. **Model Training & Experiment Tracking:**
   - Using only the TWO features identified above as predictors (X) and `latency` as the target (y), train a Bayesian Ridge regression model using `sklearn.linear_model.BayesianRidge` (use default hyperparameters).
   - Track your experiment by writing the learned parameters to `/home/user/experiment.json` in this exact format:
     `{"alpha": <alpha_ attribute>, "lambda": <lambda_ attribute>}`.

3. **Web Server Deployment (Fixing Vendored Package):**
   - You must serve your model using the `bottle` web framework.
   - The source code for `bottle` is pre-vendored at `/app/bottle-0.12.25`. However, our security scanner automatically applied a patch to it that accidentally broke the request routing. You must find the deliberate syntax error or broken code path in `/app/bottle-0.12.25/bottle.py`, fix it, and install the package (`pip install -e /app/bottle-0.12.25`).
   - Create a server script that listens on `127.0.0.1` port `8080` using `bottle`.
   - The server must expose a `POST /predict` endpoint. It will receive a JSON payload with the two selected features (using their exact column names as keys, e.g., `{"cpu_usage": 45.2, "mem_usage": 10.1}`). It must return a JSON response: `{"predicted_latency": <float prediction>}` based on your trained Bayesian Ridge model.
   - The server must also expose a `GET /health` endpoint that returns `{"status": "ok"}`.
   - Keep the server running in the background or foreground so that we can test it.

Be exact with the JSON keys and ports. Ensure the server is actively listening on `127.0.0.1:8080`.