You are acting as a database administrator. We have a Python script at `/home/user/analyze.py` that queries a SQLite database at `/home/user/store.db`. The script is supposed to calculate the total amount spent by each 'active' user specifically on products in the 'electronics' category.

However, the current SQL query in the script is running very slowly on our production data and, more importantly, returning wildly incorrect inflated totals due to a missing join condition (an implicit cross join).

Your tasks are:
1. Fix the SQL query in `/home/user/analyze.py` so that it returns the correct totals. Use explicit `JOIN` syntax rather than comma-separated tables to prevent this from happening again.
2. The query must group by the user's name and calculate the `SUM` of the order amounts.
3. Modify the database schema by adding appropriate indexes to optimize this specific query. You should at minimum index the columns used for filtering (`status` in users, `category` in products).
4. Run the fixed `/home/user/analyze.py` script. The script is already written to output the results to `/home/user/results.csv`.
5. Execute an `EXPLAIN QUERY PLAN` for your fixed query and save the exact output to `/home/user/plan.txt`.

Ensure the final `results.csv` contains the correct calculations without duplicates caused by the cross join.