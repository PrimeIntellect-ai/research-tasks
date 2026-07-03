You are a data engineer responsible for fixing an ETL pipeline. 

An upstream system dumps server dependency logs into a local SQLite database located at `/home/user/etl_data.db`. However, the upstream upsert process is corrupted and does not update existing rows. Instead, it inserts duplicate connection records with newer timestamps. As a result, querying the table directly yields stale, historical connection states mixed with current ones.

Your task is to write a Bash script `/home/user/etl_process.sh` that processes this data, bypassing the stale records, and generates a clean JSON representation of the server dependencies (an adjacency list).

Database Schema for `/home/user/etl_data.db`:
- `servers` table: 
  - `id` (INTEGER)
  - `hostname` (TEXT)
  - `env` (TEXT) - e.g., 'prod', 'dev'
- `connections_raw` table: 
  - `source_id` (INTEGER)
  - `target_id` (INTEGER)
  - `updated_at` (INTEGER) - Unix timestamp
  - `status` (TEXT) - 'active' or 'inactive'

Requirements for `/home/user/etl_process.sh`:
1. It must accept exactly one argument: the environment name (e.g., `prod`).
2. It must query the SQLite database and extract only the *most recent* connection record (highest `updated_at`) for every unique `(source_id, target_id)` pair.
3. It should filter these deduplicated records to only include connections where the current state is `'active'`.
4. It should only include connections where the *source* server belongs to the specified `env` (the target server's environment does not matter).
5. It must process the results and export them to a JSON file named `/home/user/<env>_graph.json` (e.g., `/home/user/prod_graph.json`).

JSON Output Format:
The output must be a single JSON object where keys are the source server `hostname`s (for servers that have at least one active outgoing connection). The value for each key must be an object containing:
- `outgoing_count`: Integer count of active outgoing connections.
- `targets`: A JSON array of target server `hostname`s, sorted alphabetically.

Example Output Structure:
```json
{
  "web-01": {
    "outgoing_count": 2,
    "targets": ["cache-01", "db-01"]
  }
}
```

Ensure your script is executable. After writing the script, execute it for the `prod` environment to generate `/home/user/prod_graph.json`. You may use `sqlite3`, `jq`, and standard coreutils.