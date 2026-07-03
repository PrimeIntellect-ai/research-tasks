You are acting as a storage administrator to manage disk space on a heavily utilized server. You need to process a batch of old log backups, ensure their integrity, and write a custom utility in C to deduplicate files by replacing them with hard links.

Here are your instructions:

1. You will find a master archive at `/home/user/backups/master_logs.tar`. This archive contains several nested archives (`.tar.gz` and `.zip`).
2. Extract the contents of `master_logs.tar` into a temporary location.
3. Verify the archive integrity of each nested archive. Some of these nested archives were corrupted during a previous storage migration and are invalid.
4. Extract the contents (log files and potentially symlinks) of ONLY the valid, uncorrupted nested archives into `/home/user/unpacked_logs/`. Ignore the corrupted archives entirely.
5. Write a C program at `/home/user/dedup.c` and compile it to an executable at `/home/user/dedup`. 
6. Your C program must take a single command-line argument: the path to a directory (e.g., `/home/user/dedup /home/user/unpacked_logs/`). 
7. The C program must perform the following transformations on the files within the provided directory:
   - Identify any symbolic links and delete them.
   - For all regular files, identify duplicates (files with exactly identical content).
   - Whenever duplicates are found, keep the file that comes first alphabetically by filename, and replace all subsequent duplicate files with a hard link to the first file. (The file names must remain exactly the same, but they should now point to the same inode).
8. Run your compiled `/home/user/dedup` utility on `/home/user/unpacked_logs/`.
9. Finally, write the names of all files remaining in `/home/user/unpacked_logs/` (one per line, sorted alphabetically) to `/home/user/results.txt`.

Ensure your C code compiles cleanly without warnings and correctly handles the directory operations.