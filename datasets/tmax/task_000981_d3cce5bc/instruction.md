You are a data engineer debugging and extending an ETL pipeline. 

There is a Python script located at `/home/user/etl_pipeline.py` and a SQLite database at `/home/user/ecommerce.db`. 
The script is supposed to calculate the total transaction amount for a specific subset of users, but it is currently producing massively inflated numbers due to a SQL bug (an implicit cross join). It also uses unsafe string formatting for SQL queries instead of parameterized queries.

Your task is to fix and extend the pipeline to meet the following requirements:

1. **Graph Traversal:** First, load the `referrals` table (which has `referrer_id` and `referred_id` columns representing directed edges) from `ecommerce.db` into a directed graph. You may install and use the `networkx` library. Find all users that are reachable from the seed user `user_id = 1` within a shortest path distance of **2 hops or less** (i.e., path length <= 2). The seed user themselves (distance 0) should be included.

2. **Fix the SQL Query:** Fix the SQL query in `etl_pipeline.py` to properly join the `users` and `transactions` tables so it only sums the transactions belonging to each specific user. 

3. **Parameterized Query:** Modify the script to securely pass the filtered list of user IDs (from step 1) into the SQL query using proper parameterized query construction (e.g., using `?` placeholders), completely removing the unsafe string formatting `f"{...}"`.

4. **Result Processing:** The script must execute the fixed query for the filtered users and write the results to `/home/user/final_report.json`.
   The JSON file must be a list of dictionaries, sorted in ascending order by `user_id`.
   Format of each dictionary:
   ```json
   {
       "user_id": 12,
       "name": "User_12",
       "total_spent": 145.50
   }
   ```
   *(Note: `total_spent` should be a float rounded to 2 decimal places. If a user has no transactions, their `total_spent` should be `0.0` or they can be omitted if the INNER JOIN excludes them. For this task, use an INNER JOIN so users with no transactions are omitted).*

Please write or modify the Python script `/home/user/etl_pipeline.py` to accomplish this, run it, and ensure `/home/user/final_report.json` is generated correctly.