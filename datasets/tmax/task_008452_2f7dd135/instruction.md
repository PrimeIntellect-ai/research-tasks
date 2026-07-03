You are an MLOps engineer responsible for building a robust data preprocessing pipeline for experiment artifacts. Our edge devices generate raw sensor logs in CSV format, but they are often malformed, contain missing values, and have extreme outliers. 

Your task is to write a C program that cleans these experiment logs, and a bash script that tests the pipeline's reproducibility.

**Step 1: Write the C Data Preprocessor**
Create a C program at `/home/user/clean_artifacts.c`. The program must accept two command-line arguments: the input CSV file path and the output CSV file path.
It must process the input CSV file line by line and apply the following rules:

1. **Schema Enforcement:** Every valid row must have exactly 4 comma-separated columns representing: `timestamp` (long integer), `sensor_1` (float), `sensor_2` (float), and `error_code` (integer). If a row has more or fewer than 4 columns, or if `timestamp` or `error_code` cannot be parsed as their respective integer types, drop the row entirely.
2. **Missing Value Handling:** Missing values for `sensor_1` and `sensor_2` are represented by the string `"NaN"` or an empty field (e.g., `,,`). 
   - You must use **forward-fill** imputation: replace the missing value with the most recent valid value from the same column. 
   - If a missing value occurs before any valid value has been observed for that column, drop the row entirely.
3. **Outlier Handling:** 
   - Cap `sensor_1` values at a maximum of `150.0`. Any value greater than `150.0` should be clamped exactly to `150.0`.
   - Floor `sensor_2` values at a minimum of `-50.0`. Any value less than `-50.0` should be clamped exactly to `-50.0`.
4. **Output Format:** Write the processed rows to the output CSV file. Floats must be printed with exactly two decimal places (e.g., `%.2f`). No headers should be printed unless they exist in the valid parsed rows (but headers won't parse as integers, so they will be dropped by rule 1).

**Step 2: Compile the Program**
Compile your C program into an executable located at `/home/user/cleaner`.

**Step 3: Process the Raw Data**
Run your compiled program on the provided raw dataset located at `/home/user/data/raw_experiment.csv`. Save the output to `/home/user/processed_data.csv`.

**Step 4: Pipeline Reproducibility Testing**
Create a Bash script at `/home/user/pipeline_test.sh`. The script should:
1. Make a copy of `/home/user/data/raw_experiment.csv` to `/home/user/data/raw_copy.csv`.
2. Run your `/home/user/cleaner` on `/home/user/data/raw_experiment.csv`, outputting to `/home/user/run1.csv`.
3. Run your `/home/user/cleaner` on `/home/user/data/raw_copy.csv`, outputting to `/home/user/run2.csv`.
4. Compare the SHA-256 hashes of `run1.csv` and `run2.csv`. 
5. If the hashes match, write the exact string `REPRODUCIBLE` to `/home/user/test_result.log`. If they do not match, write `FAILED`.

Make sure to run your bash script so that `/home/user/test_result.log` is generated!