You are a storage administrator managing disk space on a Linux server. Your system generates verbose, multi-line log files that are compressed to save space, but you need to filter out the noise and back up only the critical issues incrementally.

The system has a base directory at `/home/user/data`.
Inside, there are two directories: `/home/user/data/raw_logs` and `/home/user/data/processed_logs`.
There is also an existing tar snapshot file at `/home/user/data/snapshot.snar` and a base backup archive at `/home/user/data/base_backup.tar`. 

Your task is to:
1. Write a C program at `/home/user/filter.c` that reads text from standard input (stdin) and writes to standard output (stdout).
   The text consists of multi-line log records. Every record exactly follows this format:
   ```
   BEGIN_RECORD
   ID: <integer>
   LEVEL: <INFO|DEBUG|WARNING|ERROR|CRITICAL>
   MESSAGE: <some text>
   END_RECORD
   ```
   Your C program must print ONLY the complete records (from `BEGIN_RECORD` to `END_RECORD` inclusive) where the `LEVEL` is exactly `ERROR` or `CRITICAL`. Records with any other level should be completely discarded. Compile your program to an executable at `/home/user/filter`.

2. In the directory `/home/user/data/raw_logs/`, there are several gzip-compressed log files (e.g., `log1.gz`, `log2.gz`).
   For each `.gz` file in this directory, stream its decompressed contents through your compiled `/home/user/filter` program.
   Save the filtered output into `/home/user/data/processed_logs/` using the original filename but with a `.log` extension instead of `.gz` (for example, `log1.gz` becomes `/home/user/data/processed_logs/log1.log`).

3. After all logs have been processed and placed into `/home/user/data/processed_logs/`, create a GNU tar incremental backup of the `processed_logs` directory. 
   Create the incremental backup archive at `/home/user/data/inc_backup.tar`.
   You must use the existing snapshot file `/home/user/data/snapshot.snar` to ensure only the newly added files (or changed files) are included in the new archive. When invoking tar, use `-C /home/user/data` so that the paths inside the archive are relative to `/home/user/data` (i.e., the archived paths should start with `processed_logs/`).

Ensure all files are created exactly at the specified paths.