You are a data engineer tasked with repairing and querying a local ETL pipeline. 

The system consists of a background Python data feeder that queues user events into a Redis instance (running on `localhost:6379`), and a legacy worker that occasionally flushes these events into an SQLite database located at `/app/warehouse.db`.

Recently, a hardware fault caused a silent corruption in the SQLite database's B-tree, specifically affecting the `idx_status` index on the `users` table. As a result, querying the table using the `status` column currently returns stale or missing rows.

Your task consists of three parts:
1. **Fix the Database:** Repair the corrupted index `idx_status` in the SQLite database `/app/warehouse.db` so that queries using the `status` column return mathematically correct, up-to-date rows.
2. **Implement an ETL Query Tool:** Write a C program at `/home/user/etl_query.c` that safely queries the repaired database. 
   - It must accept exactly 4 command-line arguments in this order: `<status_string> <min_priority_int> <limit_int> <offset_int>`.
   - It must securely use **parameterized queries** (via `sqlite3_prepare_v2` and `sqlite3_bind_*`) to prevent SQL injection.
   - It should retrieve the `id`, `name`, `status`, `priority`, and `created_at` columns from the `users` table where `status` exactly matches the provided string AND `priority` is strictly greater than the provided integer.
   - The results must be sorted by `created_at` DESCENDING, and then by `id` ASCENDING to guarantee stable pagination.
   - It must apply the `LIMIT` and `OFFSET` arguments using query parameters.
   - It should print the results to standard output in a strict comma-separated values (CSV) format with no headers (e.g., `1042,Alice,ACTIVE,85,1698300000`).
3. **Compile and Execute:** 
   - Compile your program to `/home/user/etl_query`. (SQLite3 development headers are installed; link with `-lsqlite3`).
   - Run your tool to extract the first 500 rows where `status` is `ACTIVE` and `min_priority` is `50` (i.e., limit=500, offset=0).
   - Save the standard output of this execution to exactly `/home/user/results.csv`.

Do not modify the schema of the `users` table itself, only repair the index.