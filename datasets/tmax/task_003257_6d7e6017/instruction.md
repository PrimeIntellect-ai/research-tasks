You are a Database Reliability Engineer (DBRE) tasked with managing backup metadata. 

We have a backup metadata file located at `/home/user/backups.csv` with the following columns:
`id,db_name,type,parent_id,size_bytes,timestamp`

Due to a bug in our backup scheduler, some incremental backups are "orphaned" (their parent backups were deleted or failed) and some backup chains are fragmented. 

Your task is to write a bash script at `/home/user/analyze_chain.sh` that takes a database name as its first parameter (e.g., `./analyze_chain.sh auth_db`). The script must use only Bash and standard coreutils (like `awk`, `grep`, `sort`, etc.) to do the following:

1. **Find the Latest Base:** Identify the `full` backup for the specified database that has the highest `timestamp`.
2. **Project the Chain:** Find all valid `inc` (incremental) backups that form a continuous dependency chain starting from this latest `full` backup. An incremental backup is part of the chain if its `parent_id` points to the `id` of the full backup or any preceding valid incremental backup in this specific chain. 
3. **Aggregate:** Calculate the total size (`size_bytes`) of this valid backup chain (the `full` backup plus all its valid descendants).
4. **Output:** The script must write the result to a log file named `/home/user/<db_name>_chain.log` in the exact following format:
```
Target DB: <db_name>
Base Backup: <base_backup_id>
Chain: <base_id> -> <inc1_id> -> <inc2_id> ...
Total Size: <total_size_in_bytes>
```

Once you have written the script, execute it for the database `auth_db` to generate the required log file at `/home/user/auth_db_chain.log`.