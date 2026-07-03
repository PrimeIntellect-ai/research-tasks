You are a data engineer responsible for fixing and optimizing an ETL pipeline. 

There is an SQLite database located at `/home/user/etl_data.db`.
There is a Python script at `/home/user/broken_etl.py` which extracts high-value purchase data for recent users and writes it to a CSV file. 

Currently, the script has three major issues:
1. **Data Accuracy:** The SQL query contains an implicit cross join, resulting in a Cartesian product that returns completely incorrect revenue aggregations.
2. **Security & Best Practices:** The query is built using Python f-strings (string interpolation), leaving it vulnerable to SQL injection and preventing proper query plan caching.
3. **Performance:** The database lacks appropriate indexes, causing full table scans.

Your task is to fix this pipeline by performing the following steps:

1. **Fix the Python Pipeline:**
   Create a corrected script at `/home/user/fixed_etl.py`. 
   - Fix the SQL logic so it properly joins the `users` and `purchases` tables.
   - Refactor the query to use **parameterized queries** (e.g., using `?` placeholders) instead of string formatting.
   - Ensure the script still accepts the same two command-line arguments (`signup_date` and `purchase_date`) and outputs the results to `/home/user/output.csv` with the headers `name,amount,purchase_date`.

2. **Design an Index Strategy:**
   Determine the optimal indexes to speed up the new query's join and filtering operations. Write the SQL DDL commands to create these indexes into `/home/user/indexes.sql`.

3. **Output the Query Plan:**
   Assume your indexes from `indexes.sql` have been applied. Generate the SQLite execution plan for your newly fixed, parameterized query. Save the raw output of the `EXPLAIN QUERY PLAN` command to `/home/user/query_plan.txt`.

Ensure all file paths are exact and that your Python script runs cleanly via command line.