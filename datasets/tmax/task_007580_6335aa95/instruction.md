You are assisting a compliance officer in auditing system access logs. The data is stored in an SQLite database at `/home/user/audit.db`.

The database has the following schema:
```sql
CREATE TABLE users (uid INTEGER PRIMARY KEY, username TEXT, dept TEXT);
CREATE TABLE assets (aid INTEGER PRIMARY KEY, asset_name TEXT, classification_level INTEGER);
CREATE TABLE data_flows (source_aid INTEGER, dest_aid INTEGER);
CREATE TABLE audit_log (log_id INTEGER PRIMARY KEY, uid INTEGER, aid INTEGER, timestamp DATETIME);
```

As part of a new compliance rule, we need to process results to identify "escalation risks"—instances where a user accessed an asset that has a direct data flow to a downstream asset with a strictly higher classification level. 

Write a C program at `/home/user/process_audit.c` that uses the `libsqlite3` library to do the following:
1. Connect to `/home/user/audit.db`.
2. Programmatically execute a query to create an index named `idx_audit_aid` on the `audit_log(aid)` column to optimize our lookups (if it doesn't already exist).
3. Execute a query that joins these tables to find all audit events matching the "escalation risk" criteria:
   - The user accessed an asset (Asset A).
   - Asset A has a direct flow (`data_flows`) to Asset B (`source_aid` = Asset A, `dest_aid` = Asset B).
   - Asset B's `classification_level` is strictly greater than Asset A's `classification_level`.
4. The query must return the following columns: `username`, `source_asset_name` (Asset A), `dest_asset_name` (Asset B), and `timestamp`.
5. Order the results by `timestamp` in DESCENDING order, then by `username` in ASCENDING order.
6. The C program must accept exactly two command-line arguments for pagination: `<limit>` and `<offset>` (in that order). Use these to paginate the SQL query results.
7. Print the queried results to standard output in standard CSV format (without headers): `username,source_asset_name,dest_asset_name,timestamp`.

Compile your program to `/home/user/process_audit` using `gcc`. You can assume `sqlite3` and `libsqlite3-dev` are available on the system.