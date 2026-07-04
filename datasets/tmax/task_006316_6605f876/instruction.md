You are a data engineer building an ETL pipeline to extract dependency graphs from a microservices architecture. 

We have an SQLite database located at `/home/user/data/architecture.db` containing two tables:
1. `nodes` (id TEXT PRIMARY KEY, type TEXT)
2. `edges` (source TEXT, target TEXT, relation TEXT)

Currently, the data extraction is timing out. We need to find specific call chains, but the database is missing proper indexes, and there is a poorly designed partial index (`idx_bad_edges`) that might be misleading the query planner.

Your task is to write and execute a Python script at `/home/user/run_etl.py` that does the following:
1. Connects to the SQLite database `/home/user/data/architecture.db`.
2. Analyzes and optimizes the database by creating the appropriate indexes required for fast graph traversal. You must drop the `idx_bad_edges` index.
3. Executes a query to find all directed paths of exactly length 3 (A -> B -> C -> D) where:
   - Node A has type 'Gateway'
   - Node D has type 'Database'
   - All three edges in the path have the relation 'calls'
4. Writes the results to a CSV file at `/home/user/extracted_paths.csv` with the header exactly as: `gateway_id,service1_id,service2_id,database_id`. The rows must be sorted lexicographically by `gateway_id`, then `service1_id`, then `service2_id`, then `database_id`.
5. Retrieves the query execution plan (using `EXPLAIN QUERY PLAN`) for your path-finding query and writes the raw plan output to `/home/user/query_plan.log`.

Requirements:
- Use standard Python libraries only (e.g., `sqlite3`, `csv`).
- Do not modify the existing data in the tables, only the indexes.
- Ensure the query executes efficiently (a full table scan on a self-join of this size will freeze).