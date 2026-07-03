You are a backup administrator tasked with writing a custom C program to safely perform incremental backups of a live data directory where files might be concurrently written to.

Your objective is to create a C program that recursively traverses a directory tree, finds files modified on or after a given Unix timestamp, attempts to acquire a non-blocking read lock to ensure the file isn't actively being written to by another process, and outputs the backup data to standard output, while reporting locked files to standard error.

**Requirements:**

1.  **Write the C program:** Create a file at `/home/user/incremental_backup.c`.
    *   The program must accept exactly two command-line arguments: `<directory_path>` and `<unix_timestamp>`.
    *   It must recursively traverse the given `<directory_path>`. Ignore symbolic links and non-regular files.
    *   For each regular file, it must attempt to acquire a non-blocking shared lock (`flock` with `LOCK_SH | LOCK_NB`).
    *   **Locking failure:** If the lock cannot be acquired (e.g., `EWOULDBLOCK`), print `LOCKED: <full_file_path>\n` to `stderr` and move to the next file.
    *   **Incremental Check:** If the lock is acquired, check the file's modification time (`mtime`).
    *   If the `mtime` is strictly less than `<unix_timestamp>`, do nothing.
    *   If the `mtime` is greater than or equal to `<unix_timestamp>`, print the following to `stdout`:
        `---FILE: <full_file_path>---\n`
        followed immediately by the exact byte contents of the file, and then a trailing newline `\n` if the file doesn't already end in one (ensure the next `---FILE:` block starts on a new line).
    *   Release the lock and close the file.

2.  **Compile the program:** Compile it to `/home/user/incremental_backup`.

3.  **Setup the environment:**
    *   Run the pre-existing script `/home/user/init_data.sh` (this will generate the target directory `/home/user/data_source` and populate it with files of varying timestamps).
    *   Run the pre-existing script `/home/user/hold_locks.sh &` in the background (this will simulate active writers by holding exclusive locks on certain files for 60 seconds).

4.  **Execute the backup:**
    *   While `hold_locks.sh` is running, immediately execute your compiled program against `/home/user/data_source` with the timestamp `1700000000`.
    *   Redirect `stdout` to `/home/user/backup.out`.
    *   Redirect `stderr` to `/home/user/backup.err`.

Ensure your program handles paths correctly and efficiently. Your final verification will be based on the exact contents of `/home/user/backup.out` and `/home/user/backup.err`.