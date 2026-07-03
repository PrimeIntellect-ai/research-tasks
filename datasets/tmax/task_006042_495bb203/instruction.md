You are a storage administrator managing backups across several simulated storage volumes. A backup system writes snapshots to `/home/user/storage_mounts/`. 

Each backup consists of a data file (e.g., `backup_xyz.data`) and a corresponding metadata file in JSON format (e.g., `backup_xyz.metadata.json`). Due to a bug in the automated cleanup job, expired backups are not being deleted, and disk space is running low.

Write a Python script at `/home/user/find_expired.py` that does the following:
1. Recursively traverses `/home/user/storage_mounts/` and all its subdirectories.
2. Finds and parses all files ending with `.metadata.json`.
3. Identifies backups that meet BOTH of the following criteria:
   - The JSON contains `"retention_policy": "expired"`
   - The JSON contains a `"size_mb"` integer strictly greater than `500`.
4. For each matching backup, determines the absolute path to its corresponding `.data` file. The `.data` file will always have the exact same base name and exist in the same directory as the `.metadata.json` file.
5. Outputs a CSV report to `/home/user/expired_large_backups.csv`. 

The CSV file must have the following exact format (no headers):
`absolute_data_path,size_mb`

For example:
`/home/user/storage_mounts/vol1/appA/backup_001.data,850`
`/home/user/storage_mounts/vol3/appB/archive/backup_992.data,1024`

Run your script to generate the `/home/user/expired_large_backups.csv` file. Ensure the paths in the CSV are absolute and the CSV contains no extra spaces or headers.