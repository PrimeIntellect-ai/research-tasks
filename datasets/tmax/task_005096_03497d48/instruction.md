You are a Database Reliability Engineer (DBRE) tasked with automating database restores from a complex backup repository. 

Our backup metadata is stored in a SQLite database located at `/home/user/backups.db`. The database contains a single table named `backups` with the following schema:
- `id` (TEXT): The unique identifier of the backup.
- `db_name` (TEXT): The name of the database.
- `backup_type` (TEXT): Either 'full' or 'incremental'.
- `parent_id` (TEXT): The `id` of the parent backup (if 'incremental', otherwise empty string).
- `ts` (INTEGER): The UNIX timestamp when the backup was completed.

To restore a database to a specific point in time, we must restore the latest valid backup that occurred *at or before* the target timestamp. If this backup is an 'incremental' backup, we must first restore its parent, its parent's parent, and so on, starting from the root 'full' backup.

Your task is to write a Python script `/home/user/generate_restore.py` that does the following:
1. Accepts two command-line arguments: `<db_name>` and `<target_ts>` (an integer timestamp).
2. Connects to `/home/user/backups.db` and uses parameterized queries to fetch the necessary metadata.
3. Identifies the latest backup for the specified database with a `ts` less than or equal to `<target_ts>`.
4. Traverses the dependency graph backward to find the complete chain of backups needed for the restore, starting from the foundational 'full' backup up to the identified backup.
5. Generates an executable bash script at `/home/user/restore.sh` containing the exact pipeline of restore commands in the correct order.

The format of the commands in the generated `/home/user/restore.sh` must be exactly:
`restore_cmd --db <db_name> --id <id> --type <backup_type>`

For example, a generated script might look like:
```bash
#!/bin/bash
restore_cmd --db my_db --id bk_10 --type full
restore_cmd --db my_db --id bk_11 --type incremental
```

Once you have written the script, execute it for the database `db_prod` with a target timestamp of `1025` to generate the `/home/user/restore.sh` script.

Requirements:
- Ensure the generated bash script has a `#!/bin/bash` shebang.
- Ensure the generated script is executable (`chmod +x`).
- Do not add any extra output or commands in `restore.sh` other than the shebang and the `restore_cmd` lines.