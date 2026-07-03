You are a Database Reliability Engineer (DBRE) tasked with recovering a database. Unfortunately, the backup catalog database has crashed, leaving you with only the raw backup metadata files on disk. 

The metadata files are stored in `/home/user/backups/`. Each file is named `<uuid>.json` and contains JSON data about a backup. You need to reverse-engineer the data model from these files, which represent a graph of backup dependencies (full backups and incremental backups).

Your task is to write two Bash scripts using standard CLI tools (like `jq`, `awk`, `grep`) to organize and query this backup graph:

**Phase 1: Index Strategy Design**
Write a script at `/home/user/build_index.sh`. This script must:
1. Parse all JSON files in `/home/user/backups/`.
2. Create an "index" directory at `/home/user/backup_index/`.
3. Create symlinks inside `/home/user/backup_index/` pointing to the original backup files. The symlinks must be named using the format `<timestamp>-<id>.json` to allow for fast chronological sorting and lookup without parsing the JSON again.

**Phase 2: Graph Projection and Querying**
Write a script at `/home/user/get_chain.sh` that takes a single Unix timestamp as an argument (e.g., `/home/user/get_chain.sh 1690000500`). This script must:
1. Find the latest backup in the index whose `timestamp` is less than or equal to the provided argument.
2. Traverse the backup dependency graph backwards. Each incremental backup has a `parent_id` linking it to the previous backup. You must follow these links until you reach a backup with a `type` of "full" (which has a `parent_id` of `null`).
3. Materialize this graph projection into a forward-recovery chain (starting with the "full" backup, followed by the incrementals in chronological order).
4. Output a strictly validated JSON array to `/home/user/recovery_plan.json`. 

**Phase 3: Output Schema Validation**
The output file `/home/user/recovery_plan.json` must exactly match this schema structure:
A JSON array of objects, where each object has exactly three keys: `id`, `type`, and `file`. The objects must be ordered from the full backup to the final incremental backup.
Example output:
```json
[
  {"id": "a1b2", "type": "full", "file": "backup_a1b2.tar.gz"},
  {"id": "c3d4", "type": "incremental", "file": "backup_c3d4.tar.gz"}
]
```

Ensure your scripts are executable (`chmod +x`). Do not use any external database engines; everything must be implemented using Bash and standard utilities like `jq`.