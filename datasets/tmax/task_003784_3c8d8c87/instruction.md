You are a data engineer responsible for building an ETL and anomaly detection pipeline. 

Your task is to create a Python script that sets up a clean data environment, enforces a strict data schema, and trains a lightweight anomaly detection model.

First, set up a virtual environment at `/home/user/etl_env` and install `pandas` and `scikit-learn==1.3.0`. You must use this environment to run your Python code.

You have been provided with two files (they will exist on your system):
1. `/home/user/raw_data.csv`: A historical dataset with columns `user_id`, `age`, `annual_income`, and `profession`. Some of this data is dirty.
2. `/home/user/new_batch.csv`: A new batch of data with the same columns, assumed to be structurally correct but potentially containing statistical anomalies.

Write and execute a Python script that performs the following steps:
1. **Schema Enforcement:** Read `/home/user/raw_data.csv`. Drop any rows that violate the following schema rules:
   - `user_id`: Must not be missing.
   - `age`: Must be an integer between 18 and 100 (inclusive). Drop rows with missing, non-numeric, or out-of-bounds ages.
   - `annual_income`: Must be a positive float (> 0). Drop rows with missing, non-numeric, or invalid incomes.
   - `profession`: Must be one of exactly `['Engineer', 'Doctor', 'Artist', 'Teacher']`. Drop rows with any other value or missing values.
   
   Keep track of how many rows were dropped and how many valid rows remain.

2. **Model Training:** Using the remaining *valid* historical data, extract the features `age` and `annual_income` (in that order). Train an `IsolationForest` model from `sklearn.ensemble` with `random_state=42` and `contamination=0.1`. 

3. **Evaluation on New Batch:** Read `/home/user/new_batch.csv` (do not apply schema dropping to this file, it is guaranteed structurally valid). Extract the `age` and `annual_income` features. Use the trained `IsolationForest` to predict anomalies on this new batch. In `IsolationForest`, a prediction of `-1` indicates an anomaly. Count how many anomalies are detected in the new batch.

4. **Reporting:** Create a JSON file at `/home/user/pipeline_results.json` containing the exact following keys:
   - `"invalid_rows_dropped"`: The integer number of rows dropped from `raw_data.csv` due to schema violations.
   - `"valid_rows_trained"`: The integer number of rows used to train the model.
   - `"anomalies_detected"`: The integer number of anomalies (predicted as `-1`) detected in `new_batch.csv`.

Ensure your output JSON file is perfectly formatted.