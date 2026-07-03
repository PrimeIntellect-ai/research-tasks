As a Database Reliability Engineer, you are managing a complex system of incremental backups. The backup metadata is stored as a dependency graph in a SQLite database located at `/home/user/backup_graph.db`. 

The database has a single table:
`CREATE TABLE backups (id TEXT PRIMARY KEY, parent_id TEXT, size_bytes INTEGER);`
(If `parent_id` is NULL, it is a root backup. Incremental backups point to their parent via `parent_id`).

We have a legacy compiled tool at `/app/legacy_calc` that calculates the cumulative storage footprint of a backup. The cumulative size is defined as the size of the backup itself plus the sizes of all its downstream incremental descendants. However, `/app/legacy_calc` is incredibly slow and scales poorly for large datasets.

Your task is to write a highly optimized Python script at `/home/user/fast_calc.py` that:
1. Connects to `/home/user/backup_graph.db`.
2. Computes the cumulative size for **all root backups** (where `parent_id IS NULL`).
3. Writes the results to `/home/user/roots_summary.json` as a JSON object mapping the string `id` to its integer cumulative size (e.g., `{"root_1": 5000, "root_2": 10240}`).

To achieve the required performance, you should design and create appropriate index(es) on the SQLite database, and use optimized parameterized queries or CTEs (Common Table Expressions) to perform the cross-query aggregation natively within the database engine rather than querying in a slow iterative loop.

Your script will be evaluated on its execution speed. It must produce the correct results significantly faster than the naive baseline.