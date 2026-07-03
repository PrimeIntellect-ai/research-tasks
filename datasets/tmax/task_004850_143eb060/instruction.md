You are acting as a configuration manager tracking changes across server environments.

Your task is to create a Python script at `/home/user/tracker.py` that performs an incremental backup of configuration files by comparing a new configuration directory against an old one.

You are provided with two directories:
- `/home/user/configs_v1` (The previous backup state)
- `/home/user/configs_v2` (The current state)

The script must do the following:
1. Recursively traverse `/home/user/configs_v2`.
2. For every file found, compare it to the corresponding file in `/home/user/configs_v1` using its relative path.
3. A file is considered "NEW" if it does not exist in `configs_v1`. A file is considered "MODIFIED" if its SHA-256 content hash differs from the corresponding file in `configs_v1`.
4. If a file is NEW or MODIFIED, copy it to `/home/user/incremental_backup/`, preserving its relative directory structure (e.g., if `/home/user/configs_v2/app/db.conf` is modified, it should go to `/home/user/incremental_backup/app/...`).
5. When copying the file to `incremental_backup`, rename it by appending the first 8 characters of its SHA-256 hash before the file extension. For example, `db.conf` becomes `db_b13d2f9d.conf`.
6. Generate a summary log file at `/home/user/changes.log` that lists all the changed or new files in alphabetical order by their relative paths. The format of each line in the log file must exactly match:
`[STATUS] relative/path/to/file.ext -> relative/path/to/file_hash.ext`

Example `changes.log` line:
`[MODIFIED] app/db.conf -> app/db_b13d2f9d.conf`

Ensure you use Python to implement this logic. Once the script is written, run it so that `/home/user/incremental_backup/` and `/home/user/changes.log` are populated.