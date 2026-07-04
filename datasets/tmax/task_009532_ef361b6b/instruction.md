You are a Database Reliability Engineer (DBRE) tasked with validating backup integrity. 

You have inherited a broken bash script located at `/home/user/validate_backups.sh`. This script is supposed to calculate the total byte size of all successful backups in the `us-east-1` region by cross-referencing a SQLite relational database (`/home/user/backups.db`) with a NoSQL-style JSON log file (`/home/user/backup_logs.json`).

Currently, the script is failing/hanging because the embedded SQL query contains a severe implicit cross join (Cartesian product) between the `backups`, `servers`, and `backup_metadata` tables. 

Your tasks:
1. Analyze the schema of `/home/user/backups.db` (which contains `backups`, `servers`, and `backup_metadata` tables).
2. Fix the SQL query inside `/home/user/validate_backups.sh` so that it correctly uses `JOIN`s to retrieve only the `backup_id`s of backups that have a status of `'SUCCESS'` and belong to a server in the `'us-east-1'` region.
3. Update the bash script to process `/home/user/backup_logs.json`. Using `jq` (representing a NoSQL aggregation pipeline), calculate the sum of the `size` field across all `chunks` for the specific `backup_id`s retrieved from the SQL query.
4. The script must output ONLY the final integer representing the total size in bytes, and save this value to `/home/user/final_size.txt`.

Ensure your bash script runs automatically without user interaction and completes the entire pipeline from SQL extraction to JSON aggregation.