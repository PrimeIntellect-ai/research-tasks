You are tasked with rescuing a project directory that was damaged by a runaway backup script. The previous script followed symlinks into infinite loops, generated massive multi-line error logs, corrupted several backup archives, and messed up project configuration files. 

Your workspace is located at `/home/user/project_rescue/`. You must perform the following recovery and organization steps:

1. **Resolve Symlink Loops:**
   Inspect the log file at `/home/user/project_rescue/logs/runaway_backup.log`. The log contains multi-line error records detailing where the script got stuck. Extract the exact paths of the cyclic symlinks mentioned in the "Path:" field of the "Symlink loop detected" error blocks, and delete those symlinks from the filesystem.

2. **Verify Archive Integrity:**
   The directory `/home/user/project_rescue/archives/` contains several `.tar.gz` files. Some of these were corrupted when the backup script crashed. Verify the integrity of all `.tar.gz` files in this directory. Delete any corrupted archives (those that fail a gzip/tar integrity check) and leave the valid ones intact.

3. **Text Transformation:**
   The runaway script mistakenly altered the project configuration file at `/home/user/project_rescue/config/settings.yaml`. Using command-line text transformation tools (like `sed`, `awk`, or similar) or a Python script, replace all instances of the hardcoded incorrect string `BAD_PATH_PREFIX_992` with the correct path `/home/user/project_rescue/src`. Ensure the file is modified in-place or overwritten correctly.

4. **Implement a Smart Incremental Backup:**
   Write a Python script at `/home/user/project_rescue/smart_backup.py`. This script must:
   - Perform an incremental backup of the `/home/user/project_rescue/src/` directory.
   - Only include files that have a modification time strictly newer than the timestamp stored in `/home/user/project_rescue/last_backup.timestamp` (which contains a single Unix epoch float).
   - Explicitly ignore all symlinks to prevent future loop issues (do not follow them, do not include them in the backup).
   - Create a new archive at `/home/user/project_rescue/archives/incremental_backup.tar.gz` containing these modified files (maintaining their relative paths from the `src/` directory).
   - Generate a JSON report at `/home/user/project_rescue/backup_report.json` with the following exact format:
     ```json
     {
       "backed_up_files": ["file1.py", "subdir/file2.txt"],
       "ignored_symlinks": ["bad_link", "subdir/another_link"]
     }
     ```
     *(Note: The arrays should contain the relative paths of the files/symlinks from the `src/` directory, sorted alphabetically).*

Execute your script so the new archive and report are generated.