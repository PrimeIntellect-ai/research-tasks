You are acting as a compliance officer auditing a legacy financial system. The company has an undocumented SQLite database located at `/app/data/audit_logs.db` and a compiled, closed-source compliance scoring engine located at `/app/legacy_risk_scorer`. 

Your objective is to identify high-risk users and aggregate their total transaction volumes. 

Here are the requirements:
1. **Reverse Engineer the Data Model:** The SQLite database contains three undocumented tables related to users, their transactions, and their login access events. You must explore the database to understand the schema and how these tables relate to one another.
2. **Optimize Performance:** The database contains hundreds of thousands of records and currently has no indexes. You must design and implement an index strategy (e.g., executing `CREATE INDEX` statements directly on the database) so that complex cross-table queries execute very quickly.
3. **Data Aggregation and Scoring:** Write a Python script at `/home/user/audit_aggregator.py`. The script must:
   - Query the database to calculate, for each user, their `total_access_events` and their number of `distinct_ips` logged in from.
   - Pass this data to the legacy scoring engine. The engine is a stripped binary executable that reads CSV data from `stdin` (format: `user_id,total_access_events,distinct_ips` on each line) and outputs CSV data to `stdout` (format: `user_id,risk_score`).
   - For any user with a `risk_score > 0.80`, calculate the sum of their transaction amounts (`total_tx_amount`).
4. **Output Generation:** The Python script must write a JSON file to `/home/user/flagged_users.json`. The JSON should be a dictionary mapping the `user_id` (as a string) to their `total_tx_amount` (as a float, rounded to 2 decimal places).
   Example:
   ```json
   {
     "U1029": 4500.50,
     "U9921": 120.00
   }
   ```

**Performance Constraint:**
Your Python script will be tested against a strict time threshold. Because the database is large, an unoptimized query structure without proper database indexes will take over 15 seconds to run. Your solution (the execution of `python3 /home/user/audit_aggregator.py`) must run to completion in **under 3.0 seconds**, while producing the exact correct JSON output.