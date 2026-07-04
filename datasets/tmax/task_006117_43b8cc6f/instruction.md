As a FinOps analyst, I need to optimize our simulated local cloud storage costs by safely archiving large files from active directories. We implement a staged archival deployment and strict backup strategies to ensure zero data loss.

I need you to write a C++ program that scans our storage, backs up large files, moves them to a staging area, and generates an audit log using strict timezone and locale settings.

Write the source code to `/home/user/cost_optimizer.cpp` and compile it to `/home/user/cost_optimizer` using `-std=c++17`. 

The program must perform the following:
1. **Configuration**: Read the file `/home/user/storage_config.txt`. Each line in this file contains the absolute path of an active "bucket" (directory) to scan.
2. **Criteria**: Identify all regular files within these directories (non-recursive) that are strictly larger than `100000` bytes.
3. **Backup and Staged Archival**: For each identified file:
   - Safely copy the file to `/home/user/storage_backup/` (maintaining its original filename).
   - Once the backup copy is successful, move the original file to `/home/user/archive_staging/` (maintaining its original filename).
4. **Audit Logging**: For every successfully staged file, append a log entry to `/home/user/finops_audit.log`. 
   - The timestamp must be in strict `UTC` time, regardless of the system's local timezone.
   - The log line must exactly match this format:
     `[YYYY-MM-DD HH:MM:SS UTC] STAGED <original_full_path> <size_in_bytes> bytes`
   - Example: `[2023-10-25 14:30:00 UTC] STAGED /home/user/cloud_storage/bucketA/large_data.bin 150000 bytes`

**Constraints & Error Handling:**
- Do not process directories recursively, only the immediate files in the configured buckets.
- If a target bucket directory from the config file does not exist, the program should gracefully skip it and continue processing the others.
- Ensure the destination directories (`/home/user/storage_backup/` and `/home/user/archive_staging/`) exist before copying/moving files; if not, your C++ program must create them.
- Assume filenames across buckets are unique.

After writing and compiling the program, execute it so the optimization process is completed and the log file is generated.