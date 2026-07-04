You are a storage administrator tasked with managing disk space and processing logs efficiently. You must perform an incremental backup and process compressed streams without extracting them to disk.

Your task has two parts:

Part 1: Incremental Backup
A previous full backup of the `/home/user/logs/` directory exists at `/home/user/full_backup.tar.gz`. Since this backup was taken, some files in `/home/user/logs/` have been modified and new files have been added.
Create a compressed archive at `/home/user/incremental.tar.gz` that contains ONLY the files within `/home/user/logs/` that are newer than `/home/user/full_backup.tar.gz`. The paths inside the archive should be relative to the `/home/user/` directory (e.g., `logs/file1.log`).

Part 2: Compressed Stream Processing
Without extracting `incremental.tar.gz` to the filesystem, read its contents as a stream, search for any lines containing the exact string `FATAL`, and write only those lines into a new gzip-compressed file at `/home/user/fatal_errors.gz`. 
The lines inside `/home/user/fatal_errors.gz` (once decompressed) must be sorted alphabetically. 

Constraints:
- You may write scripts in Bash or Python.
- Do not extract `incremental.tar.gz` to a temporary directory on disk. Process it directly as a stream.
- Only the lines from the updated/new files should be present in `fatal_errors.gz`.

Ensure all output files are placed exactly at the requested paths.