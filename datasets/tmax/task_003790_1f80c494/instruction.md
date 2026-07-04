You are assisting a compliance officer in auditing system access logs. There is an SQLite database located at `/home/user/access_logs.db` that contains historical access records, but the documentation for its schema has been lost. 

Your task is to write a Python script at `/home/user/audit.py` that performs the following tasks:
1. Reverse engineer the database to find the table containing the access logs. The table will have columns that track usernames, IP addresses, timestamps, and login status.
2. Identify the query needed to retrieve the 10 most recent failed login attempts (where the status indicates a failure), sorted by timestamp in descending order.
3. The database is currently unoptimized. Your script must create an appropriate index in the database to optimize this exact query.
4. Use the `EXPLAIN QUERY PLAN` command for your extraction query and save its output to `/home/user/query_plan.txt` (the file should contain the exact output row(s) returned by sqlite3).
5. Execute the query to retrieve the 10 most recent failed login attempts and save the results as a JSON array of objects to `/home/user/failed_logins.json`. Each object must contain all columns from the table, using the column names as keys.

Ensure your script runs successfully and creates the required output files. You may use the `sqlite3` command line tool or Python's `sqlite3` module to explore the database before writing your script.