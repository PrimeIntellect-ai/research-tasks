You are acting as a database administrator for a graph-based application. We are using SQLite to store our graph data. 

In `/app/schema_and_query.png`, there is an image containing a description of our schema and a slow query that we use to perform cross-query aggregation and path summarization over our graph. Currently, this query takes too long to execute.

Your task is to:
1. Extract the exact SQL query from the image `/app/schema_and_query.png`.
2. Analyze the execution plan of this query on the SQLite database located at `/app/graph.db`.
3. Optimize the database and/or the query. You can create indexes, materialized views, or rewrite the query to make it faster while producing the exact same results.
4. Write a Python script at `/home/user/setup_db.py` that applies any schema optimizations (e.g., creating indexes) to `/app/graph.db`.
5. Save your final (or original, if you only optimized the schema) SQL query to `/home/user/optimized.sql`.

Requirements:
- Your query in `/home/user/optimized.sql` MUST return the exact same rows and columns as the query shown in the image.
- The automated verifier will measure the execution time of `/home/user/optimized.sql` after running your `/home/user/setup_db.py` script, and compare it against the baseline execution of the original query on a fresh database.
- You must achieve a speedup of at least 20x.
- You may use OCR tools like `tesseract` (preinstalled) to read the image.

Ensure your code handles SQLite connections correctly and commits any schema changes.