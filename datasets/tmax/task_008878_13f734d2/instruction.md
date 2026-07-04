You are a backup administrator tasked with creating an automated incremental backup script for our application servers. 

Our application data is stored in `/home/user/app_data/`. You need to write a Python script at `/home/user/do_backup.py` and execute it to perform an incremental backup based on an existing configuration and state.

Here are the requirements for your Python script:
1. **Configuration Parsing:** Read the backup rules from `/home/user/backup_rules.json`. This file contains two keys: `include_extensions` (a list of file extensions like `.xml`, `.json`) and `exclude_dirs` (a list of directory names to completely ignore during traversal).
2. **State Management:** Read the last backup timestamp from `/home/user/state.json`. It contains a key `last_run` with a UNIX timestamp.
3. **Recursive Traversal:** Traverse `/home/user/app_data/`. 
   - Skip any directories whose base name is in the `exclude_dirs` list.
   - Only consider files whose extension is exactly in the `include_extensions` list.
   - Only backup files that have been modified *strictly after* the `last_run` timestamp.
4. **Copying Data:** Copy the qualifying files to `/home/user/incremental_backup/`, preserving their directory structure relative to `/home/user/app_data/`. (e.g., `/home/user/app_data/logs/db.json` becomes `/home/user/incremental_backup/logs/db.json`).
5. **Manifest Generation & Atomic Writes:** After copying, create a manifest file at `/home/user/incremental_backup/manifest.json`. 
   - The manifest must be a JSON array of strings, representing the relative paths of the files backed up (e.g., `["logs/db.json", "config/settings.xml"]`), sorted alphabetically.
   - **Crucial:** To prevent partial manifest reads by other processes, you MUST write this manifest atomically. Write the JSON array to `/home/user/incremental_backup/manifest.tmp` first, and then rename/move it to `/home/user/incremental_backup/manifest.json`.
6. **Execution:** Once written, execute your script `/home/user/do_backup.py` so the backup is performed.

Do not update `state.json` (we will handle that in a different job). Focus purely on generating the correct `manifest.json` and copying the correct files.