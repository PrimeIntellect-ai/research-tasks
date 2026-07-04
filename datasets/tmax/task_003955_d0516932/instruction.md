You are a data engineer tasked with building a lightweight ETL pipeline using Python. 

You have two raw data sources:
1. `/home/user/customers.csv`: Contains customer metadata. Columns: `id`, `age`, `status`.
2. `/home/user/logs.jsonl`: Contains text logs from users. Keys: `user_id`, `text`.

Write and execute a Python script to perform the following ETL steps:
1. **Schema Enforcement**: Filter the `customers.csv` data. Keep only rows where:
   - `id` is a valid integer.
   - `age` is a valid integer AND is strictly >= 18.
   - `status` is exactly the string `"ACTIVE"` or `"INACTIVE"`.
2. **Feature Engineering & Tokenization**: For the `logs.jsonl` data, calculate a new feature called `log_tokens`, which is the integer count of whitespace-separated words in the `text` field.
3. **Multi-source Join**: Perform an inner join of the filtered customers and the processed logs on `id` == `user_id`.
4. **Output**: Write the result to `/home/user/processed_data.jsonl`. 
   - Each line must be a valid JSON object with exactly these keys: `{"id": <int>, "age": <int>, "status": <str>, "log_tokens": <int>}`.
   - The lines in the file must be sorted by `id` in ascending order.
   - Ensure native integer types are used in the JSON output (e.g., `25`, not `"25"`).

Once your script finishes, ensure `/home/user/processed_data.jsonl` exists and correctly implements all logic.