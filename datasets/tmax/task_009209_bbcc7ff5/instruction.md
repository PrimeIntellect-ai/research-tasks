You are an IT backup administrator. You have been given a primary backup archive located at `/home/user/backups/raw.tar.gz`. This archive contains several nested archives and raw files. Due to an error in the backup system, some compressed files were saved without file extensions, and logs from various systems were mixed together.

Your objective is to extract these files, identify hidden archives by their file signatures, and write a Go program to extract and sanitize specific multi-line error records.

Perform the following steps:

1. **Extract and Prepare Files:**
   - Extract `/home/user/backups/raw.tar.gz` into the directory `/home/user/backups/extracted/`.
   - Traverse the extracted files. You will find files without extensions. Determine their actual file types by examining their binary headers (magic numbers).
   - If any file without an extension is actually a `gzip` or `zip` archive, extract its contents into the same directory (`/home/user/backups/extracted/`).

2. **Process Logs using Go:**
   - Write a Go program at `/home/user/process_logs.go`.
   - The program should recursively scan the `/home/user/backups/extracted/` directory for any file ending in `.log` (including those you just extracted from the hidden archives).
   - Parse these log files to find multi-line error records. A multi-line error record always starts with the exact string `[ERROR]` and continues until a completely empty line (or the end of the file) is encountered.
   - For every multi-line error record found, redact any IPv4 addresses (e.g., `192.168.1.50`) by replacing them exactly with the string `[REDACTED]`.
   - Append the redacted multi-line error records to a single file at `/home/user/backups/summary.log`. Separate each extracted error record with exactly one empty line.

Ensure your Go program successfully handles the large-scale text transformations and multi-line parsing correctly. Run your script to generate the final `summary.log`.