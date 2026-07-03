You are a Database Reliability Engineer handling a backup validation system. We recently exported the topology of our distributed datastore into static files to perform offline analysis, as the live database graph is too heavily loaded. 

Currently, an older validation script we used was producing completely wrong results because it performed an implicit cross join (Cartesian product) between all storage nodes and databases, rather than respecting the actual graph edges.

Your task is to reverse-engineer the exported data model and build a pure Bash-based aggregation pipeline to extract the correct backup mapping.

**Data Location & Format:**
1. `/home/user/backups/nodes.jsonl`: A JSON Lines file representing nodes in our topology. Each line is a JSON object with `id`, `type` (e.g., "Database", "StorageNode"), and `status` ("ONLINE" or "OFFLINE").
2. `/home/user/backups/edges.csv`: A CSV file representing directed graph edges between nodes, with columns `source_id,target_id,relation_type`. 

**The Objective:**
You must write a Bash script at `/home/user/scripts/verify_backups.sh` that processes these files and outputs the active, valid backup pairs. 

A valid backup pair exists if and only if:
1. There is a `STORES_BACKUP_FOR` relation pointing from a `StorageNode` (source) to a `Database` (target).
2. **Both** the `StorageNode` and the `Database` have a `status` of `"ONLINE"`. If either is "OFFLINE", the pair is invalid and must be excluded.

**Requirements:**
- Your script `/home/user/scripts/verify_backups.sh` must be executable and use standard Linux CLI tools (`bash`, `jq`, `awk`, `join`, `grep`, `sort`, etc.). You may not use Python, Node.js, or spin up an actual database.
- The script must write its final output to `/home/user/output/valid_backup_pairs.jsonl`.
- The output file must be in JSON Lines format, where each line is exactly: `{"database_id":"<db_id>","storage_id":"<storage_id>"}`.
- The output lines must be sorted alphabetically by `database_id`.
- Ensure no implicit cross joins occur! Only output pairs explicitly connected by the `STORES_BACKUP_FOR` edge where both components are active.

Create the script and execute it to generate the output file.