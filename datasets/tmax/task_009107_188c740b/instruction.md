You are a Database Reliability Engineer (DBRE) managing a complex system of full and incremental backups. We store the metadata of all backup snapshots in a JSON-based document store, which has been exported to a file at `/home/user/backup_metadata.json`.

Each backup record contains a `backup_id`, `type` (full or incremental), `parent_id` (the backup it directly depends on, or `null` if it's a full backup), and `size_mb` (the size of the backup in megabytes).

To manage our storage, we need a way to calculate the total storage footprint of a specific backup "chain". The total footprint of a backup is defined as its own `size_mb` plus the `size_mb` of ALL its direct and indirect descendants (any incremental backups that recursively depend on it).

Your task is to create a Bash script at `/home/user/chain_size.sh` that takes a single argument (the `backup_id`) and outputs EXACTLY the total size of that backup chain in megabytes as a single integer. 

Requirements:
- The script must be written in Bash (using standard tools like `jq`, `awk`, `grep`, etc. is perfectly fine and encouraged).
- The script must accept the `backup_id` as its first positional argument (e.g., `./chain_size.sh bkp_001`).
- The script must print ONLY the final integer sum to standard output.
- It must recursively find all dependent backups (children, grandchildren, etc.).
- The script must have execute permissions.

Assume `/home/user/backup_metadata.json` exists and is a valid JSON array of objects.