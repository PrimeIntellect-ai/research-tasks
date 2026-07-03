You are acting as a configuration manager tasked with tracking system changes and creating an incremental backup of configuration files. 

You need to perform the following steps carefully in the `/home/user` directory:

1. **Incremental Backup via Hard Links**: 
   There is an active configuration directory at `/home/user/configs` and a previous backup at `/home/user/last_backup`. 
   Create a new directory at `/home/user/current_backup`. Copy all files from `/home/user/configs` into `/home/user/current_backup`. However, to act as a space-saving incremental backup, any file in `/home/user/configs` that is identical (in content) to its counterpart in `/home/user/last_backup` MUST be hard-linked to the file in `/home/user/last_backup` instead of being copied. Files that are new or have changed must be standard standalone files.

2. **Data Parsing**:
   Write a Python script that parses all `.ini` files in `/home/user/current_backup`. Find all configuration lines that contain key-value pairs separated by an equals sign (`=`). Extract all keys that start with the exact string `EXPORT_`. 
   Write a JSON file to `/home/user/current_backup/summary.json` containing a single dictionary mapping these extracted keys to their corresponding string values. (All keys across all files are guaranteed to be unique).

3. **Symlink Management**:
   Create a symbolic link at `/home/user/latest_backup` that points directly to `/home/user/current_backup`.

4. **Archiving**:
   Create a gzipped tar archive of the `/home/user/current_backup` directory at `/home/user/backup.tar.gz`. The archive should contain the `current_backup` folder at its root.

Ensure your Python script runs successfully and all file outputs exactly match the requirements.