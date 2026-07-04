You are a data analyst investigating a network of financial transactions. You have been given two CSV files:
1. `/home/user/accounts.csv`: Contains `account_id,account_name`
2. `/home/user/transactions.csv`: Contains `tx_id,src_id,dst_id,amount,tx_date`

Your objective is to write a Bash script `/home/user/analyze.sh` that uses `sqlite3` to process these files, optimize the database, and extract specific insights using advanced SQL.

Your Bash script must perform the following actions exactly:
1. Create a SQLite database at `/home/user/finance.db`.
2. Import `accounts.csv` into a table named `accounts` and `transactions.csv` into a table named `transactions`.
3. Create an index named `idx_src_date` on the `transactions` table covering `src_id` and `tx_date` to optimize our analytical queries.
4. Execute a SQL query that does the following:
   - Joins `accounts` and `transactions` (using `account_id` = `src_id`).
   - Uses a Window Function to calculate the **running total** of the `amount` sent by each account, ordered by `tx_date` ascending.
   - Filters the results to find the **first** transaction (by date) for each account where their running total strictly exceeds `5000`.
   - The query should output `account_name,tx_date,running_total`.
5. Save the output of this query as a CSV file (without headers) to `/home/user/alerts.csv`.
6. Use `EXPLAIN QUERY PLAN` on that exact same SELECT query and save the output to `/home/user/query_plan.txt`.

Requirements:
- Ensure your script is executable (`chmod +x`).
- Do not include headers in `alerts.csv`.
- Sort the final output in `alerts.csv` by `account_name` alphabetically.
- You may use temporary tables or CTEs if necessary to perform the filtering after the window function.