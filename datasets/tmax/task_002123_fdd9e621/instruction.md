You are a data engineer tasked with building a robust, reproducible ETL pipeline test. Your pipeline must clean a raw dataset, strictly enforce its schema, and track pipeline metrics. 

There is a raw data file located at `/home/user/input.csv` (you can assume it already exists).

Perform the following tasks:
1. Install necessary dependencies. You will need `pandas` and `pandera` for data manipulation and strict schema enforcement.
2. Write a Python script at `/home/user/pipeline_test.py` that does the following:
   - Reads the `/home/user/input.csv` file.
   - Cleans the data by dropping any rows that violate the domain rules: `value` must be greater than or equal to `0.0`, and `category` must be one of `'X'`, `'Y'`, or `'Z'`.
   - Uses `pandera` to explicitly define and enforce a `DataFrameSchema` on the cleaned dataset. The schema must enforce:
     - `id`: integer
     - `value`: float, must be >= 0.0
     - `category`: string, must be in ['X', 'Y', 'Z']
   - Saves the cleaned, validated dataframe to `/home/user/output.csv` (excluding the index).
   - Tracks pipeline metrics by creating a JSON file at `/home/user/metrics.json` with exactly the following keys:
     - `"original_rows"`: integer (number of rows in the raw dataset)
     - `"valid_rows"`: integer (number of rows after cleaning)
     - `"schema_passed"`: boolean (should be `true` if the pandera validation succeeds without throwing an error).

Run your script so that `/home/user/output.csv` and `/home/user/metrics.json` are successfully generated.