You are a Database Reliability Engineer handling a corrupted backup. 

You have been provided with an SQLite database at `/home/user/telemetry.db`. 
We have detected that the index `idx_telemetry_node` on the `telemetry` table is corrupted, causing it to return phantom rows during standard index scans. 

Your task is to write and execute a Python script (`/home/user/fix_and_extract.py`) that performs the following pipeline:
1. Connects to `/home/user/telemetry.db`.
2. Drops the corrupted index `idx_telemetry_node`.
3. Creates a new, optimized covering index named `idx_telemetry_optimal` on `telemetry(node_id, ts, metric)` to speed up future extracts.
4. Executes a join query to extract valid telemetry data. You only want telemetry records where the associated node (from the `nodes` table) has `status = 'ACTIVE'` and `region = 'us-east'`.
5. Validates the output to ensure each record strictly adheres to this schema before exporting:
   `{"telemetry_id": int, "node_id": int, "timestamp": str, "metric_value": float}`.
6. Exports the validated results as a JSON array to `/home/user/clean_backup.json`. The output must be formatted with an indent of 2 spaces.

The database schema is as follows:
- `nodes`: `node_id` (INTEGER PRIMARY KEY), `status` (TEXT), `region` (TEXT)
- `telemetry`: `id` (INTEGER PRIMARY KEY), `node_id` (INTEGER), `ts` (DATETIME), `metric` (REAL)

Do not use third-party ORMs; standard library `sqlite3` and standard `json` are sufficient.