You are acting as a backup administrator managing database transaction logs. You need to process a directory of raw Write-Ahead Logs (WAL) and prepare them for chunked offsite archiving.

The raw log files are located in `/home/user/backups/raw_logs` and its subdirectories. The files have a `.wal` extension.

These `.wal` files contain multi-line transaction records in a specific plain-text format:
```
[2023-10-01T12:00:00] BEGIN TX 105
INSERT INTO users (id, name) VALUES (1, 'Alice');
UPDATE config SET active = 1;
[2023-10-01T12:00:05] COMMIT TX 105
[2023-10-01T12:01:00] BEGIN TX 106
DELETE FROM logs WHERE old = 1;
[2023-10-01T12:01:02] ROLLBACK TX 106
```
Each transaction block starts with a `BEGIN TX <id>` line and ends with either a `COMMIT TX <id>` or `ROLLBACK TX <id>` line.

Your task is to write and execute a Python script (`/home/user/process_backups.py`) that performs the following operations:
1. Recursively traverse `/home/user/backups/raw_logs` to find all `.wal` files.
2. Parse the multi-line transaction blocks.
3. Extract ONLY the complete transaction blocks (from BEGIN to COMMIT, inclusive) that ended with a `COMMIT`. Discard any transactions that ended in `ROLLBACK`.
4. Sort these committed transaction blocks in ascending order based on their transaction `<id>` (which is an integer).
5. Write the sorted transaction blocks to `/home/user/backups/processed/commits.wal`. Separate each transaction block with a single empty line.
6. After writing `commits.wal`, split this file into exact 150-byte chunks (the last chunk may be smaller). Place these chunks in `/home/user/backups/processed/chunks/` with the naming convention `chunk_00.dat`, `chunk_01.dat`, `chunk_02.dat`, etc.

Ensure the `/home/user/backups/processed/chunks/` directory is created if it does not exist.