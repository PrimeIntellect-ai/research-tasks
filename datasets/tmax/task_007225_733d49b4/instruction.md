You are a Data Engineer building automated data quality tests for an ETL pipeline. Before loading raw daily sales data into the warehouse, you need to verify that the mean sales amount is statistically stable by computing a bootstrap confidence interval. 

You have been provided a raw data file at `/home/user/raw_etl_data.jsonl`. Each line is a JSON object containing an `id` and a `sales_amount`.

Your task is to:
1. Create a Python virtual environment located precisely at `/home/user/etl_venv`.
2. Install `numpy` and `pandas` within this virtual environment.
3. Write a Python script at `/home/user/test_etl_bootstrap.py` that does the following:
   - Reads the `/home/user/raw_etl_data.jsonl` file.
   - Extracts the `sales_amount` values into an array.
   - Sets the numpy random seed to exactly `42` (`numpy.random.seed(42)`).
   - Generates 10,000 bootstrap samples (randomly sampling with replacement, where each sample is the same size as the original dataset).
   - Calculates the mean of each bootstrap sample.
   - Computes the 95% confidence interval (the 2.5th and 97.5th percentiles) of these bootstrap means.
   - Writes the resulting lower and upper bounds to `/home/user/bootstrap_results.txt` as a single line, comma-separated, rounded to exactly 2 decimal places (e.g., `98.45,102.34`).
4. Execute your script using the created virtual environment to generate the results file.