As a backup administrator, you need to write a Go program to archive specific database Write-Ahead Log (WAL) files. We have a directory structure at `/home/user/db_backups` that contains a mix of valid WAL files, corrupted WAL files, and symlinks to other directories. 

Unfortunately, a previous administrator created a messy directory structure that includes symlink loops.

Write a Go script at `/home/user/backup.go` and run it to perform the following:
1. Recursively search `/home/user/db_backups` for valid WAL files.
2. A file is considered a "valid WAL file" ONLY if its first 4 bytes are exactly `WAL\x01` (in hex: `57 41 4C 01`). 
3. You MUST follow symlinks to search inside linked directories. However, your script must detect and prevent infinite loops caused by circular symlinks. 
4. If a directory symlink would cause a loop (i.e., it points to an ancestor directory currently being traversed), do not follow it. Instead, write the absolute path of that specific symlink to `/home/user/loop_log.txt` (one path per line).
5. All valid WAL files discovered must be added to a new compressed tarball at `/home/user/archive.tar.gz`. The paths of the files inside the tar archive must be relative to the `/home/user/db_backups/` base directory (e.g., `cluster1/wal_01.log`). If a file is found via an external symlink, its path in the tarball should follow the symlink's name inside the backups directory (e.g., `external_link/wal_ext.log`).

Requirements:
* Ensure your Go script reads the file headers efficiently (do not load massive files entirely into memory just to check the magic bytes).
* The resulting `/home/user/archive.tar.gz` must be a valid gzip-compressed tar archive.
* Do not archive files that lack the correct magic bytes.