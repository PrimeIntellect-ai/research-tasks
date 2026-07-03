You are a data engineer debugging an ETL pipeline. A recent pandas pipeline has silently introduced data corruption, casting some integer `user_id` values to floats (e.g., `102.0` or `NaN`) due to missing values in other columns.

You have been provided a dataset at `/home/user/daily_etl.csv` with the following header:
`user_id,session_time,click_count,bounce_rate,revenue`

Your tasks are:
1. **Feature Extraction (Dimensionality Reduction):** Extract only the `user_id`, `click_count`, and `revenue` columns.
2. **Anomaly Classification:** Identify the "corrupted" records. A record is corrupted if its `user_id` contains a decimal point (`.`) or is exactly `NaN`. Save the extracted features of ONLY the corrupted records to `/home/user/corrupted.csv` (include the extracted header).
3. **Metric Computation:** Calculate the sum of the `revenue` for all corrupted records and save this single number to `/home/user/corrupted_revenue.txt`.
4. **Hyperparameter Tuning (Threshold Search):** We want to build a simple rule-based model to predict if a record will be corrupted based purely on `click_count`. The model rule is: `If click_count > T, predict Corrupted; else predict Valid`. 
   Evaluate integer thresholds `T` from `1` to `10`. Find the threshold `T` that yields the highest classification accuracy on the provided dataset. Write the best integer `T` to `/home/user/best_threshold.txt`. (If there's a tie, choose the lowest `T`).

You may use standard Linux CLI tools (like `awk`, `grep`, `sed`) or write a quick Python/Bash script to accomplish this. Do not install external libraries. Ensure all output files are placed exactly as specified.