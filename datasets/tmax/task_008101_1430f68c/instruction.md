You are acting as a backup administrator. We have a daily backup routine, but our current backup script is failing. Someone recently added symlinks in our data directory, and the script is following them into infinite loops, crashing with a `RecursionError`. Furthermore, we need to convert this script to perform incremental backups rather than full backups to save space.

Your task is to write a Python script at `/home/user/incremental_backup.py` that performs an incremental backup. 

Here are the specific requirements for your script:
1. It must accept three command-line arguments: 
   `--dir` (the directory to back up)
   `--base` (the path to the previous full backup, a `.tar.gz` file)
   `--out` (the path where the new incremental `.tar.gz` backup should be saved)
2. **Symlink handling**: The script must traverse the directory specified by `--dir` but MUST completely ignore all symlinks (do not back them up, do not follow them).
3. **Incremental logic**: The script must read the compressed stream of the `--base` tarball to determine the modification times (`mtime`) of previously backed up files.
4. A file from the target directory should ONLY be added to the `--out` archive if:
   - It does not exist in the `--base` archive.
   - OR its current filesystem modification time is strictly greater than the modification time recorded in the `--base` archive.
5. **Archive format**: The `--out` file must be a valid gzip-compressed tarball (`.tar.gz`). The paths inside the archive must start with the base name of the backed-up directory (e.g., if `--dir /home/user/data_dir` is passed, paths in the archive should look like `data_dir/file1.txt`).
6. **Logging**: Whenever the script runs, it must create a file at `/home/user/backup_log.txt`. This file should contain a list of the exact relative file paths (matching the format inside the tar archive, e.g., `data_dir/file1.txt`) that were added to the incremental backup. Write one path per line, sorted alphabetically.

To complete the task, execute your script against the data in the workspace:
- Target directory: `/home/user/data_dir`
- Base backup: `/home/user/base_backup.tar.gz`
- Output archive: `/home/user/incremental.tar.gz`