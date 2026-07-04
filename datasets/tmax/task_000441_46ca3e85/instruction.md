You are a data analyst troubleshooting an issue with an SQLite database. The database located at `/home/user/ecommerce.db` contains sales data, but recent queries have been unacceptably slow and occasionally returning inconsistent results, leading us to suspect a corrupted or highly unoptimized index on the `transactions` table.

Your task is to write a C++ program that cleans up the database indexes, optimizes the schema for our reporting needs, and generates a final aggregated report.

Specifically, write a C++ program at `/home/user/analyzer.cpp` that performs the following steps sequentially using the `sqlite3` C/C++ API:
1. Connect to `/home/user/ecommerce.db`.
2. Execute a command to drop all existing indexes on the `transactions` table to clear out the corrupted/stale state.
3. Create new, optimized covering indexes that will strictly benefit the analytical query described in step 5.
4. Run an `EXPLAIN QUERY PLAN` for the analytical query (from step 5) and write the output rows to `/home/user/query_plan.txt` (one row of the plan per line).
5. Execute the analytical query to find the top 5 users by total transaction volume for the 'Electronics' product category during Q4 2023 (October 1, 2023 to December 31, 2023 inclusive).
   - The result must join `users`, `transactions`, and `products`.
   - Calculate the total transaction volume (`SUM(amount)`) and the average transaction amount (`AVG(amount)`).
   - Order the results by total transaction volume in descending order. If there is a tie, order by the user's name alphabetically.
   - Limit the results to exactly 5 rows (pagination).
6. Output the final aggregated query results to `/home/user/report.csv` in the exact format: `user_name,total_volume,avg_amount`. Ensure floating point numbers are formatted to 2 decimal places.

You must compile your program using:
`g++ -O3 -std=c++17 /home/user/analyzer.cpp -lsqlite3 -o /home/user/analyzer`

Once compiled, execute `/home/user/analyzer`.

Requirements:
* Do not use external C++ libraries other than the standard library and `<sqlite3.h>`.
* Ensure `libsqlite3-dev` is installed before compiling.
* All generated files must be in `/home/user/`.