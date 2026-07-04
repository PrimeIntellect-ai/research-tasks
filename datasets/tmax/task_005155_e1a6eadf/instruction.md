You are a data engineer tasked with building an automated ETL and model training pipeline. We have raw web server logs and a list of IP addresses categorized as "bot" or "human". Your goal is to write a Bash script that extracts features from the logs, merges them with the labels, and then runs a Python script to train and evaluate a classification model.

Here are the details:
1. **Raw Logs Location**: `/home/user/raw_logs.txt`
   Format: `timestamp | ip_address | response_time_ms | payload_bytes`
   (Note: Fields are separated by ` | `).
2. **Labels Location**: `/home/user/labels.csv`
   Format: `ip_address,label` (Labels are `1` for bot, `0` for human).

**Step 1: Write an ETL script in Bash**
Create a script at `/home/user/run_etl.sh` that does the following:
- Aggregates the raw logs by `ip_address` to calculate three features:
  1. Count of requests (integer)
  2. Total payload_bytes (integer)
  3. Average response_time_ms (integer, rounded down to the nearest whole number)
- Joins these aggregated features with the labels from `labels.csv`.
- Outputs a finalized dataset to `/home/user/features.csv` with the exact format: `ip_address,request_count,total_payload,avg_response_time,label`. Do not include a header row.
- Ensure the output is sorted by `ip_address` ascending.

**Step 2: Environment Setup & Modeling**
- The Bash script `/home/user/run_etl.sh` must install the `scikit-learn` and `pandas` packages (using `pip install`).
- The Bash script must then create and execute a Python script `/home/user/train.py`.
- The Python script should:
  1. Read `/home/user/features.csv`.
  2. Use `request_count`, `total_payload`, and `avg_response_time` as features (X), and `label` as the target (y).
  3. Train a `sklearn.linear_model.LogisticRegression` model (use `random_state=42`).
  4. Predict on the training set and calculate the accuracy score.
  5. Write the accuracy score (just the number, e.g., `0.85`) to `/home/user/accuracy.txt`.

Ensure `/home/user/run_etl.sh` is executable and runs the entire pipeline from start to finish when executed.