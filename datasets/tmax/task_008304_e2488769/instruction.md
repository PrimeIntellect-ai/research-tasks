You are an AI assistant helping a configuration manager safely back up changing configuration files.

We have a configuration directory at `/home/user/configs/`. Several background processes frequently update these files. The directory also contains some legacy symlinks, some of which form infinite loops. 

Your task is to write and execute a Bash script at `/home/user/config_backup.sh` that performs a safe differential backup of the regular configuration files. 

The script must meet the following requirements:
1. **File Locking:** Before reading any files, the script must acquire an exclusive file lock on `/home/user/configs.lock` to prevent concurrent modifications during the backup. It must release the lock when finished.
2. **Manifest Generation:** Traverse `/home/user/configs/` and compute the SHA-256 checksum of every **regular file** (strictly ignore all symlinks to avoid infinite loops and ignore directories). 
3. **Differential Parsing:** Read the existing manifest at `/home/user/old_manifest.txt` (format: `<sha256sum>  <filepath>`). Compare the newly computed checksums against this old manifest.
4. **Backup:** Create a directory `/home/user/backup_diff/`. Copy only the regular files that are newly added or whose contents have changed (checksum mismatch) into this directory. Preserve their base file names (assume all files have unique base names).
5. **New Manifest:** Write the newly computed checksums to `/home/user/new_manifest.txt` in the exact same format as the old manifest (`<sha256sum>  <full_filepath>`). Sort the contents of `new_manifest.txt` alphabetically by file path.

Once you have written the script, execute it so that `/home/user/new_manifest.txt` and `/home/user/backup_diff/` are generated correctly.