You are tasked with building a lightweight ETL pipeline and inference benchmarking suite for a simulated machine learning deployment.

You must complete the following phases. You can use standard bash commands and Python.

**Phase 1: Environment Setup**
Ensure your Python environment has the necessary libraries to handle data processing and Parquet files (e.g., `pandas`, `pyarrow`, `numpy`).

**Phase 2: ETL Pipeline (`/home/user/etl.py`)**
There is a raw data file located at `/home/user/raw_data.csv`. It contains four columns: `id`, `f1`, `f2`, `f3`.
Write a Python script named `etl.py` that:
1. Reads `/home/user/raw_data.csv`.
2. Applies Min-Max scaling to the `f1`, `f2`, and `f3` columns. (For each column: `(x - min) / (max - min)`).
3. Saves the transformed dataset (keeping the `id` column) to a Parquet file at `/home/user/processed_data.parquet`.

**Phase 3: Inference & Benchmarking (`/home/user/inference.py`)**
Write a Python script named `inference.py` that:
1. Loads `/home/user/processed_data.parquet`.
2. Computes a mock inference prediction for each row using the formula: `pred = 0.5 * f1 + 0.3 * f2 - 0.2 * f3`.
3. Calculates the numerical accuracy metric: the mean of the `pred` column.
4. Benchmarks the inference step: Run the exact inference computation (`0.5 * f1 + 0.3 * f2 - 0.2 * f3` across all rows) 100 times in a loop. Record the total time taken and calculate the average time per run in milliseconds.

**Phase 4: Reporting**
Your `inference.py` script must output a JSON file at `/home/user/report.json` with the following exact keys:
- `"row_count"`: The integer number of rows processed.
- `"mean_pred"`: The mean of the `pred` column across the dataset, rounded to exactly 4 decimal places.
- `"avg_time_ms"`: The average time per inference run in milliseconds, rounded to exactly 4 decimal places.

Run your scripts so the final `/home/user/report.json` is generated.