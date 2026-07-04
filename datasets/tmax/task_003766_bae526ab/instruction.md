You are acting as a data analyst. You have been provided with two CSV files containing historical data, but querying them is currently too slow. You need to write a Python pipeline that loads the data into SQLite, designs an optimal index strategy, interprets the query plan, and outputs the final results.

**Data files:**
1. `/home/user/users.csv` 
   Columns: `user_id` (integer), `name` (text), `status` (text: 'ACTIVE' or 'INACTIVE')
2. `/home/user/transactions.csv`
   Columns: `tx_id` (integer), `user_id` (integer), `amount` (float), `tx_date` (text: 'YYYY-MM-DD')

**Your objective:**
Write a Python script at `/home/user/pipeline.py` that performs the following steps:
1. Creates a SQLite database at `/home/user/analytics.db`.
2. Loads the two CSV files into standard relational tables named `users` and `transactions`.
3. Creates appropriate indexes to optimize the following exact analytical query:
   `SELECT u.name, SUM(t.amount) as total_spent FROM users u JOIN transactions t ON u.user_id = t.user_id WHERE u.status = 'ACTIVE' AND t.tx_date BETWEEN '2023-01-01' AND '2023-12-31' GROUP BY u.user_id ORDER BY total_spent DESC LIMIT 5;`
4. Runs `EXPLAIN QUERY PLAN` on the query above and writes the raw text output (specifically the `detail` column from the SQLite explain plan) to `/home/user/query_plan.txt`. You must design your indexes so that SQLite uses them efficiently (e.g., avoiding full table scans where possible).
5. Executes the analytical query and saves the results to `/home/user/top_users.csv`. Include the header row (`name,total_spent`) and format the `total_spent` to 2 decimal places.

Do not use external libraries other than standard Python libraries like `sqlite3` and `csv` (no Pandas). Ensure your final script handles the end-to-end pipeline.