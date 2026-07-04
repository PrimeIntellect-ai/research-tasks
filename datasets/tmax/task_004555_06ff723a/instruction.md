You are a Database Reliability Engineer responsible for managing NoSQL backup chains. Our system generates raw backup metadata exports, but our orchestration system needs to query the lineage (dependency graph) of these backups via a REST API to safely garbage-collect old snapshots.

We have a vendored application designed for this exact purpose located at `/app/backup-lineage-server`. It is a Python-based HTTP server that loads a processed CSV of backup metadata, materializes a directed graph of dependencies, and serves lineage queries.

However, the pipeline is currently broken:
1. The raw data is at `/home/user/manifests.jsonl`. Each line is a NoSQL document representing a backup. You must process this file into a flat CSV format at `/home/user/processed_graph.csv`.
   The CSV must have a header: `backup_id,parent_backup_id,size_bytes,status`.
   The fields map from the JSON as follows:
   - `backup_id`: from `_id`
   - `parent_backup_id`: from `metadata.parent` (leave empty if null)
   - `size_bytes`: from `metadata.size`
   - `status`: from `state`

2. The vendored package at `/app/backup-lineage-server` contains a bug. The developer hardcoded a privileged path (`/var/lib/backups/data.csv`) in `server.py` instead of accepting the file path via the `DATA_PATH` environment variable. Additionally, there is a logical flaw in `server.py` where it ignores rows with an empty `parent_backup_id`, failing to add the root backups to the graph. You must patch `/app/backup-lineage-server/server.py` to fix these issues.

3. Once fixed, you must start the server on `127.0.0.1:9090` using your processed CSV. The server must be running in the background.

The server exposes `GET /lineage/<backup_id>`. When functioning correctly, it should return a JSON array containing the chronological lineage of backup IDs (from the immediate parent all the way up to the root backup).

Ensure the server is actively listening on `127.0.0.1:9090` before you finish. You can use any language or standard terminal utilities (like `jq`, `awk`, or Python) to complete this task.