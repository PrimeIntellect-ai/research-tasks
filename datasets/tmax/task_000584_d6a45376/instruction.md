You are a Database Reliability Engineer (DBRE) responsible for analyzing backup metadata across our global fleet. 

Our internal reporting tools rely on a locally vendored version of the `peewee` ORM library, which is located at `/app/peewee`. However, a recent faulty patch broke its ability to generate correct SQL for `INNER JOIN` operations. 

Your tasks are to:
1. Identify and fix the perturbation in the vendored `peewee` package in `/app/peewee`. 
2. Analyze the SQLite database at `/home/user/backup_metrics.db` to understand its schema. It contains tables related to `servers`, `backups`, and `restores`.
3. Write a Python script at `/home/user/get_metrics.py` that queries this database using the fixed `peewee` library (you must use `/app/peewee`, do not install it from pip).

The script must accept exactly two positional arguments:
`python3 /home/user/get_metrics.py <datacenter> <min_backup_size_bytes>`

For the given `<datacenter>`, filter for servers that have *at least one* backup whose size is strictly greater than `<min_backup_size_bytes>`. 
For those servers, print a CSV-formatted output to standard output (without headers) containing:
`hostname,latest_backup_status,total_size_of_successful_backups,restore_success_rate`

Definitions:
- `latest_backup_status`: The `status` string of the most recent backup (by `timestamp`) for the server.
- `total_size_of_successful_backups`: The sum of `size_bytes` for all backups belonging to the server where `status` is exactly `'SUCCESS'`. If none, output `0`.
- `restore_success_rate`: The percentage of successful restores (where `is_successful = 1` or `True`) out of all restore attempts associated with any of the server's backups. Format to exactly 2 decimal places (e.g., `85.50`). If a server has 0 restore attempts across all its backups, output `N/A`.

Order the final output alphabetically by `hostname` ascending.

Ensure your script is perfectly deterministic and parameterized to handle arbitrary `<datacenter>` strings and integer `<min_backup_size_bytes>` values securely.