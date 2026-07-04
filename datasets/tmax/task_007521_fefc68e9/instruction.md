You are an MLOps engineer tasked with processing raw experiment tracking logs to generate a visualization artifact for a dashboard. 

You have a set of raw experiment logs located in `/home/user/raw_logs/`. Each file is a JSON document representing a single model training run, containing a `run_id` and a nested `metrics` dictionary with five numerical values: `loss`, `accuracy`, `epoch_time`, `mem_usage`, and `cpu_load`.

Your task is to:
1. Install any necessary Python packages (e.g., `pandas`, `scikit-learn`) in the system environment.
2. Write and execute a Python script (`/home/user/process_artifacts.py`) that acts as an ETL pipeline:
   - Extracs all JSON logs from `/home/user/raw_logs/`.
   - Flattens the data so that each run is a row with the `run_id` and the 5 metrics.
   - Standardizes the 5 metrics (removes the mean and scales to unit variance).
   - Applies Principal Component Analysis (PCA) to reduce the 5 metric dimensions down to 2 dimensions (components). Use `random_state=42` for the PCA initialization if required by the library.
3. Save the resulting 2D projection as a CSV file at `/home/user/artifacts/pca_projection.csv`.
   - The CSV must contain exactly three columns in this order: `run_id`, `pca_1`, `pca_2`.
   - The CSV must include a header row.
   - The values for `pca_1` and `pca_2` must be rounded to 4 decimal places.
   - The rows should be sorted alphabetically by `run_id`.

Ensure your script creates the `/home/user/artifacts/` directory if it does not already exist.