You are a Database Reliability Engineer (DBRE) managing a graph database backup pipeline. Our backup shards are split into two representations: relational node metadata (CSV files) and document-based edge structures (JSON files). 

Recently, corrupted backups have been silently infiltrating our storage. You need to fix our local graphing tools and build a bash-based validator to detect and reject these corrupted backups.

**Step 1: Fix the Vendored Package**
We use a local utility package called `bash-graph-tools-1.0` located at `/app/vendor/bash-graph-tools-1.0`. It contains helper scripts for backup processing. 
However, its setup script is broken due to a hardcoded library path that fails in our current environment. 
1. Inspect `/app/vendor/bash-graph-tools-1.0/Makefile` or `setup.sh`.
2. Fix the perturbation so it correctly builds/installs to its local `bin` directory (it has a hardcoded absolute path that should be relative or updated to match the container's layout).
3. Run its build/setup process so that `/app/vendor/bash-graph-tools-1.0/bin/gextract` becomes executable and returns a valid version string.

**Step 2: Create the Backup Classifier**
Write a Bash script at `/home/user/validate_backup.sh` that takes two arguments:
`$1`: Path to a JSON file containing graph edges (Format: `{"edges": [{"src": "A", "dst": "B"}, ...]}`)
`$2`: Path to a CSV file containing node metadata (Format: `node_id,node_type,created_at`)

Your script must evaluate the backup shard and exit with `0` (clean/accept) or `1` (evil/reject).
A backup shard is considered **corrupted (evil) and must be rejected** if EITHER of these conditions are met:
1. **Dangling Edge:** Any `src` or `dst` in the JSON edges array does NOT exist as a `node_id` in the provided CSV file. (Requires cross-representation mapping).
2. **Supernode Corruption:** Any single node acts as the `src` for more than 50 edges. (Requires cross-query aggregation).

You may use tools like `jq`, `awk`, or `sqlite3` inside your bash script to perform the complex joins and aggregations. 

Ensure your script is executable (`chmod +x /home/user/validate_backup.sh`).