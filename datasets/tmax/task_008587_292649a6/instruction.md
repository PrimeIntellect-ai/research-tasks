You are an MLOps engineer maintaining a data processing pipeline. We have a daily ETL job that merges transaction data with customer profiles, but a downstream model is failing because the `customer_id` column in the output is unexpectedly formatted as floats (e.g., `104.0`) instead of integers. 

This issue is caused by a silent pandas type casting behavior when missing values are introduced during the merging process.

Your tasks are:

1. **Fix the ETL Script**: 
   Modify the existing Python script at `/home/user/process_data.py`. 
   - Identify where the `customer_id` column gets converted to `float64` due to missing values.
   - Handle the missing `customer_id` values by filling them with `0`.
   - Ensure the final `customer_id` column is strictly of integer type (e.g., `int64`).
   - Feature Engineering: Add a new column named `log_transaction_value` which should be the natural logarithm of `transaction_value + 1` (log1p).

2. **Artifact Tracking**:
   The script must save the output DataFrame to `/home/user/artifacts/processed_data.csv` (do not include the index).
   Additionally, the script must export the final pandas column data types to a JSON file at `/home/user/artifacts/schema.json` (format: `{"column_name": "dtype_string"}`).

3. **Pipeline Reproducibility**:
   Write a bash script at `/home/user/run_pipeline.sh` that:
   - Creates a Python virtual environment in `/home/user/venv`.
   - Activates it and installs `pandas` and `numpy`.
   - Runs the fixed `/home/user/process_data.py`.
   - Calculates the MD5 checksum of `/home/user/artifacts/processed_data.csv` and saves the output in `/home/user/artifacts/run_log.txt`.

Make sure `/home/user/run_pipeline.sh` is executable. You should test your pipeline by running `./run_pipeline.sh`.

Here is the initial state of the data and script:
- `/home/user/raw_data/transactions.csv`
- `/home/user/raw_data/customers.csv`
- `/home/user/process_data.py` (has the silent cast bug)