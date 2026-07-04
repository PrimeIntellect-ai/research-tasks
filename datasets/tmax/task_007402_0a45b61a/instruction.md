You are a data engineer tasked with building a reproducible ETL pipeline to process and clean messy customer data.

You have been provided with two input files:
1. `/home/user/data/users.csv` containing columns: `user_id`, `name`, `age`, `signup_date`
2. `/home/user/data/purchases.csv` containing columns: `user_id`, `amount`, `purchase_date`

Your goal is to write a Python script `/home/user/etl.py` and a Bash runner script `/home/user/run_etl.sh` that satisfy the following requirements.

**Bash Script (`/home/user/run_etl.sh`):**
1. Create a Python virtual environment at `/home/user/venv`.
2. Activate the virtual environment.
3. Install `pandas`.
4. Run the `/home/user/etl.py` script.
5. The script must be executable.

**Python Script (`/home/user/etl.py`):**
1. Read the two CSV files.
2. **Clean `users` data:**
   - Identify "valid" ages as strictly between 1 and 120 inclusive (1 <= age <= 120).
   - Compute the median of these *valid* ages.
   - Fill any missing (empty/NaN) ages with this median value.
   - After filling missing values, drop any rows where the age is still invalid (age < 1 or age > 120).
3. **Clean `purchases` data:**
   - Drop any rows where `amount` < 0 (outliers/refunds).
4. **Join & Aggregate:**
   - Perform an inner join between the cleaned users and cleaned purchases on `user_id`.
   - Group by `user_id`, `name`, and `age`, and calculate the `total_amount` (sum of `amount` for each user).
5. **Output:**
   - Write the resulting dataset to `/home/user/output.jsonl` in JSON Lines format.
   - The output must be sorted by `user_id` in ascending order.
   - Each line should be a JSON object with exactly these keys: `user_id` (integer), `name` (string), `age` (float), and `total_amount` (float).

Ensure your bash script works completely unattended and produces the final `/home/user/output.jsonl` file when executed.