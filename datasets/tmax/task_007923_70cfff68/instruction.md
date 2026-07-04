You are acting as a Backup Administrator. Your system generates multi-line log files containing the status of nightly backup jobs. Your task is to clean, parse, and archive these logs.

You will find a raw log file at `/home/user/backup_jobs.log`.

The log file contains multiple backup job records. Each record begins with `[JOB_START]` and ends with `[JOB_END]`.
Inside each record, there are multiple fields on separate lines, such as:
- `JobID: <integer>`
- `ServerIP: <IPv4 address>`
- `Result: <SUCCESS or FAILED>`
- `FilesProcessed: <integer>`
- `ErrorTrace: <multi-line text>` (only present if FAILED)

Your task consists of three parts:

1. **Redaction (Text Transformation)**
The logs contain sensitive server IP addresses. Using a shell command (`sed`, `awk`, etc.) with stream redirection, create a new file at `/home/user/redacted.log` where EVERY IPv4 address in the `ServerIP: ...` lines is replaced exactly with `XXX.XXX.XXX.XXX`. Leave the rest of the file unchanged.

2. **Multi-line Log Parsing (Python)**
Write and execute a Python script at `/home/user/process_backups.py`. This script must read `/home/user/redacted.log`, parse the multi-line records, and filter them. 
You must extract the `JobID` of every job that has a `Result: SUCCESS`. Ignore any jobs where `Result: FAILED`.
Output these successful JobIDs into a file named `/home/user/successful_job_ids.txt`. 
Write exactly one integer JobID per line, and sort them in ascending numerical order.

3. **Archiving**
Compress the resulting `/home/user/successful_job_ids.txt` file into a gzip-compressed tarball named `/home/user/backup_report.tar.gz`. The tarball should contain only the file `successful_job_ids.txt` (do not include the full `/home/user/` directory path inside the archive).

Ensure all requested files are created at their exact paths.