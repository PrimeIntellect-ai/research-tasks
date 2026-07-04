You are acting as a storage administrator trying to clean up disk space. You have inherited a directory of legacy backups located at `/home/user/backups`. 

A poorly written legacy backup script previously ran on the server. Because it improperly followed symlinks without checking for circular references, some of the resulting backup archives contain infinitely looping directory structures (or at least very deeply nested paths) that consume massive amounts of space. Additionally, some archives were interrupted during creation and are corrupted.

Your task is to analyze all `.tar.gz` files in `/home/user/backups` and generate a structured JSON report located at `/home/user/report.json`.

For each `.tar.gz` file in the directory, you must:
1. Verify its integrity (i.e., whether the gzip compression and tar structure are intact and can be read without errors).
2. If the archive is valid, stream its contents without extracting it to disk (to save I/O and disk space) and determine the maximum "depth" of any file or directory contained within it. 
   - The "depth" is defined by the number of forward slashes (`/`) in the file or directory path within the tarball. For example, `file.txt` has a depth of 0, `dir/file.txt` has a depth of 1, and `dir1/dir2/dir3/` has a depth of 3.
3. If the archive is corrupted or fails the integrity check, its status should be marked as "corrupt" and its max depth should be reported as 0.

The final output MUST be a perfectly formatted JSON file at `/home/user/report.json` containing an object where the keys are the filenames of the archives (e.g., `backup1.tar.gz`) and the values are objects with "status" (either "valid" or "corrupt") and "max_depth" (an integer).

Example output format for `/home/user/report.json`:
```json
{
  "backup1.tar.gz": {
    "status": "valid",
    "max_depth": 3
  },
  "broken_backup.tar.gz": {
    "status": "corrupt",
    "max_depth": 0
  },
  "loop_backup.tar.gz": {
    "status": "valid",
    "max_depth": 42
  }
}
```

Use only Bash shell built-ins, coreutils, and standard CLI tools (`tar`, `gzip`, `awk`, `jq`, etc.) to complete this task.