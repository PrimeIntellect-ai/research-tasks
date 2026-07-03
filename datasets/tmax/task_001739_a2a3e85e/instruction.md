As a backup administrator, you are tasked with safely processing a batch of incoming backup archives. The system receives regular `.tar.gz` drops in the `/home/user/backups/` directory. However, some files might still be in the process of being transferred by other services, and some transfers might have failed, resulting in corrupted archives.

Your objective is to write and execute a Python script at `/home/user/process_backups.py` that processes these archives safely and generates an audit log.

The script must perform the following steps for every `.tar.gz` file in `/home/user/backups/`:
1. **Concurrency Safety:** Before reading a file, the script must acquire an exclusive, non-blocking file lock on the archive using Python's `fcntl.flock`. If a file is locked by another process (or the lock cannot be acquired), skip it and do not include it in the output. (Assume no other processes are actually locking them during your final run, but the mechanism must be present).
2. **Integrity Verification:** Verify that the archive is a valid, uncorrupted gzip-compressed tarball.
3. **Structured Parsing:** If the archive is valid, extract and parse the `metadata.json` file located at the root of the archive. Extract the values for the keys `app_name` and `version`.
4. **Audit Logging:** Append the results to a CSV file located at `/home/user/backup_audit.csv`.

**Output Specifications for `/home/user/backup_audit.csv`:**
- The CSV must have exactly these headers: `archive_name,status,app_name,version`
- `archive_name` is just the filename (e.g., `backup1.tar.gz`).
- `status` should be `valid` if the archive is intact and contains valid JSON metadata, or `corrupt` if the archive is invalid, corrupted, or missing the `metadata.json` file.
- `app_name` and `version` should contain the extracted values. If the status is `corrupt`, these fields should literally be the string `N/A`.
- The rows in the CSV *must* be sorted alphabetically by `archive_name`.

Once your script is written, execute it so that `/home/user/backup_audit.csv` is generated.