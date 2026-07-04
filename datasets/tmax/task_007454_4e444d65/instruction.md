You are an ML Engineer preparing a pipeline to train a fraud detection model. We have a data pipeline written in Bash that joins datasets, normalizes features, and splits the data into training and test sets. However, the current pipeline suffers from **data leakage**: it computes the normalization statistics (Min and Max) over the entire dataset *before* splitting, rather than computing them strictly on the training set and applying them to both.

Your workspace is located at `/home/user/ml_pipeline`.

Inside this directory, you will find:
1. `generate_data.py`: A script to generate the raw CSV files (`users.csv` and `transactions.csv`). Run `python3 generate_data.py` first to generate the raw data.
2. `prepare_data.sh`: A buggy Bash script that joins the CSVs, scales the `amount` column, and splits the data.
3. `train_model.py`: A Python script to train a Logistic Regression model on `train_scaled.csv` and evaluate it on `test_scaled.csv`.
4. `predict.py`: A Python script that loads the trained model and runs inference on a given CSV.

**Your objectives:**

1. **Fix the Data Leakage in ETL (Bash):**
   Modify `prepare_data.sh` so that it performs the following steps correctly:
   - Joins `users.csv` and `transactions.csv` on `user_id` (ensure both are sorted by `user_id` ascending). The joined format should be `user_id,age,amount,fraud_label`.
   - Splits the joined data: The first 800 rows become the training set, and the remaining 200 rows become the test set.
   - Computes the minimum and maximum values of the `amount` column **only** using the training set.
   - Applies Min-Max scaling `(value - min) / (max - min)` to the `amount` column in both the training and test sets using the train set's min/max.
   - Saves the final outputs as `/home/user/ml_pipeline/train_scaled.csv` and `/home/user/ml_pipeline/test_scaled.csv`. Output the scaled amounts formatted to exactly 4 decimal places. The output CSVs must not have headers.

2. **Train the Model:**
   Run `python3 train_model.py`. It will read your fixed scaled datasets, train a model, output its accuracy, and save `model.pkl`.

3. **Inference Performance Benchmarking (Bash):**
   Write a Bash script named `/home/user/ml_pipeline/benchmark.sh`. This script must:
   - Run `python3 predict.py test_scaled.csv` exactly 50 times sequentially in a loop.
   - Measure the total wall-clock time taken to complete all 50 runs.
   - Calculate the average time per run in milliseconds.
   - Write this average time to `/home/user/ml_pipeline/avg_time.txt` in the format: `Average Inference Time: <value> ms` (e.g., `Average Inference Time: 45.23 ms`).

Make sure your ETL Bash script correctly parses and processes the CSV files using standard Unix text-processing tools (like `awk`, `join`, `sort`, `head`, `tail`).