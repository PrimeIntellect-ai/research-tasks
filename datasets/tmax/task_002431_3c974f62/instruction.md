You are acting as a backup administrator. We have a directory at `/home/user/data_to_backup` that needs to be archived into a tar.gz file. However, previous attempts to back this directory up have failed because it contains symlinks that point back to parent directories, causing traditional backup scripts to fall into infinite loops and crash.

Your task is to write and execute a Python script located at `/home/user/safe_backup.py` that safely backs up this directory. 

The script must fulfill the following requirements:
1. **Traverse the Directory:** Recursively find all files in `/home/user/data_to_backup`. 
2. **Handle Symlink Loops:** Resolve all symlinks to their real, absolute paths. You must maintain a set of "seen" real absolute paths. If a file or directory's real path has already been processed, skip it to prevent infinite loops and duplicate entries.
3. **Archive Creation:** Create a compressed tarball (`.tar.gz`) containing only the *files* (not directories) discovered during traversal. The archive should be written to `/home/user/backup.tar.gz`. Inside the tarball, use the real absolute paths of the files as the archive names.
4. **Atomic Writes:** To ensure a partially written archive is never left on disk if the script fails, the script must write the tarball to a temporary file first (e.g., `/home/user/backup.tar.gz.tmp`), and then atomically rename it to the final target `/home/user/backup.tar.gz`.
5. **Archive Verification:** After the archive is written and renamed, the script must programmatically open and verify the integrity of the tarball (e.g., reading its contents using the `tarfile` module) to ensure it is valid. 
6. **Logging:** Create a log file at `/home/user/backup_log.txt`. Write the real absolute paths of every file successfully added to the tar archive, one path per line, sorted in alphabetical order.

Run your script to produce the final `backup.tar.gz` and `backup_log.txt`.