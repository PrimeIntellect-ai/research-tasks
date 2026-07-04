You are a Database Administrator tasked with optimizing and profiling a set of analytical queries for our local SQLite data warehouse.

You have been provided with the following files:
1. `/home/user/company.db`: An SQLite database containing three tables: `employees`, `departments`, and `salaries`.
2. `/home/user/queries.sql`: A file containing several SQL SELECT queries separated by semicolons.
3. `/home/user/schema.json`: A JSON schema file defining the exact structure required for the output metrics.

Your task consists of three phases:

**Phase 1: Optimization**
Analyze the queries in `/home/user/queries.sql` and the schema of `/home/user/company.db`. The database currently lacks necessary indexes, causing poor performance. 
Identify the optimal indexes needed for these specific queries and create them directly in `/home/user/company.db`.

**Phase 2: Execution and Aggregation**
Write a Python script to execute each query found in `/home/user/queries.sql` against the optimized `/home/user/company.db`. 
For each query, you must record:
- `query_id`: A string identifier for the query (use "query_1", "query_2", etc., based on their order in the file).
- `row_count`: The integer number of rows returned by the query.
- `execution_time_ms`: The execution time of the query in milliseconds (as a float).

**Phase 3: Validation and Export**
Using Python (you may install the `jsonschema` package via pip), validate your aggregated list of query metrics against the schema provided in `/home/user/schema.json`.
Once validated, export the JSON array to exactly `/home/user/optimized_results.json`.

Ensure your final JSON file exactly matches the schema and contains the correct row counts for the queries. You do not need to submit the Python script itself, only the final `company.db` (with indexes added) and the `optimized_results.json` file.