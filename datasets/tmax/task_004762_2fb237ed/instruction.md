You are acting as a backup administrator resolving an issue with an automated backup job.

The previous backup job failed because a custom backup script followed symlinks and fell into an infinite loop. The log output of this failed job is located at `/home/user/failed_backup.log`. 

Your task is to:
1. Parse `/home/user/failed_backup.log` to identify the exact path of the symlink that points back to a parent directory, causing the loop. The error is recorded as a multi-line entry in the log.
2. Delete that specific looping symlink to break the cycle.
3. Create a new gzipped tar archive of the `/home/user/data` directory at `/home/user/backup.tar.gz`. You **must** dereference all remaining symlinks (meaning the archive should contain the actual files the symlinks point to, not the symlinks themselves).
4. Extract `data/metrics.json` from your newly created archive.
5. Convert the extracted `metrics.json` into a CSV file located at `/home/user/metrics.csv`. The CSV must have exactly three columns in this order: `id,value,status`, with a header row. 

Ensure the final archive is valid and the CSV is correctly formatted.