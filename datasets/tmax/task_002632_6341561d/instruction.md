You are a data analyst responsible for processing a daily batch of financial transactions. You have been provided with two CSV files located in `/home/user/data/`:
1. `/home/user/data/customers.csv` - Contains customer information (columns: `user_id`, `first_name`, `last_name`, `email`).
2. `/home/user/data/transactions.csv` - Contains transaction records (columns: `tx_id`, `user_id`, `amount`).

Write and execute a Python script to build a data processing pipeline that strictly performs the following steps in order:

1. **Validation Checkpoints (Quality Gates):**
   - Filter out any customers from `customers.csv` whose `email` does not contain an `@` symbol.
   - Filter out any transactions from `transactions.csv` where the `amount` is strictly less than `0.0`.

2. **Anomaly Detection:**
   - Group the remaining, valid transactions by `user_id`.
   - Calculate the median transaction amount for each user.
   - Add a boolean column `is_anomaly` to the transactions. Set it to `True` if a transaction's `amount` is strictly greater than 3.0 times that user's median transaction amount. Otherwise, set it to `False`.

3. **Data Masking and Anonymization:**
   - On the valid customers dataset, mask the `last_name` by replacing the entire string with `***`.
   - Mask the `email` by replacing the local part (everything before the `@`) with `***`, keeping the domain intact (e.g., `alice@example.com` becomes `***@example.com`).

4. **Joins and Merges:**
   - Perform an inner join between the validated/anonymized customers and the validated/anomaly-scored transactions on `user_id`.

5. **Output Generation:**
   - Save the final joined dataframe to `/home/user/output/processed_data.csv`. The CSV must contain exactly these columns in this order: `tx_id`, `user_id`, `first_name`, `last_name`, `email`, `amount`, `is_anomaly`. Do not include a row index.
   - Create a summary JSON file at `/home/user/output/summary.json` containing the total number of final valid records and the total number of anomalies found across the final dataset, in exactly this format:
     `{"total_valid_records": <integer>, "total_anomalies": <integer>}`

Ensure your script creates the `/home/user/output/` directory if it does not exist. You may install and use the `pandas` library.