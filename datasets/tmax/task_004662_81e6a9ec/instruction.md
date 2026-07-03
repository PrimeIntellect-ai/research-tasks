You are an AI assistant acting as a backup administrator. 

We need to create an incremental backup script for the directory `/home/user/data`. However, there are two issues:
1. The directory contains a symlink loop (`/home/user/data/loop` points back to `/home/user/data`), which has been causing our previous tools to crash with infinite recursion.
2. The third-party software we use requires a custom compressed archive format.

Your task is to write and execute a Python script that accomplishes the following:

1. **Parse Backup History**: Read `/home/user/backup_history.log`. This file contains multi-line records of previous backups. You must parse this log to find the `Timestamp` of the *most recent* backup record where the `Status` is exactly `SUCCESS`.
2. **Recursive Traversal**: Recursively traverse `/home/user/data`. You MUST avoid following symlinks to prevent infinite loops. 
3. **Filter Incremental Files**: Identify all regular files (not directories, not symlinks) whose modification time (`mtime`) is strictly *greater* than the timestamp of the most recent successful backup.
4. **Custom Archive Format**: Create a custom archive of these files. For each file, the format must be exactly:
   ```
   <relative_filepath>\n
   <file_size_in_bytes>\n
   <file_contents>
   ```
   *Note: Concatenate these blocks directly one after another for all qualifying files. Sort the files alphabetically by their relative file path before appending them to the archive to ensure deterministic ordering. The relative path should not start with `./` or `/`.*
5. **Compression**: Compress the resulting string (as UTF-8 bytes) using Python's standard `zlib.compress()` with the default compression level.
6. **Output**: Save the final zlib-compressed bytes to `/home/user/latest_backup.zlib`.

Ensure your script handles the traversal carefully and generates the exact expected output. You may use standard Python libraries only (e.g., `os`, `re`, `zlib`).