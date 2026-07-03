You are a data engineer managing a lightweight ETL pipeline written purely in Bash and `awk`. 

You have been given an existing script at `/home/user/etl.sh` and a dataset at `/home/user/data/raw.csv`. The raw dataset has a header `age,income,score` followed by 100 rows of numeric data. 

The current `etl.sh` script does the following:
1. Validates the schema (ensures exactly 3 comma-separated numeric columns).
2. Computes the minimum and maximum values for each column across the *entire* dataset.
3. Performs Min-Max scaling on all rows to bring values into the [0, 1] range: `scaled_x = (x - min) / (max - min)`.
4. Splits the scaled data into a training set (first 80 rows) and a test set (remaining 20 rows).
5. Runs a hardcoded linear regression inference on the test set.

**The Problem:**
This pipeline suffers from a classic data leakage bug! By computing the minimum and maximum values over the entire dataset before splitting, information from the test set leaks into the training set's feature scaling. 

**Your Task:**
1. Fix the data leakage in `/home/user/etl.sh`. Modify the script so that:
   - The data is split *before* scaling. The training set must strictly be the first 80 data rows (after the header). The test set must be the remaining data rows.
   - The `min` and `max` values for each column must be computed **only** using the training set.
   - Both the training set and the test set are then scaled using the training set's `min` and `max` values. (Note: This means some test set values might fall slightly outside the [0, 1] range, which is mathematically correct).
2. The linear regression model uses the following fixed weights:
   - `W_age = 2.5`
   - `W_income = 0.5`
   - `W_score = -1.2`
   - `Bias = 5.0`
3. Have your fixed Bash script output the final regression predictions for the 20 test set rows to `/home/user/predictions.txt`. 
   - The file should contain exactly 20 lines, each with a single floating-point number representing the predicted value for that test row.
   - Do not include headers in the output file.

You can run and test your script as many times as you like. Ensure `/home/user/predictions.txt` is accurate based on standard IEEE 754 double precision arithmetic (which `awk` uses by default).