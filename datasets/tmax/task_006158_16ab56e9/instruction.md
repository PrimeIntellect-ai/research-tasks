You are a backup administrator responsible for auditing legacy backup archives. Recently, a security alert was issued regarding "zip slip" vulnerabilities, where maliciously crafted archives contain file paths that resolve outside the intended extraction directory (e.g., using directory traversal sequences like `../`).

Your task is to write and execute a Bash script at `/home/user/audit_backups.sh` that scans the existing backup repository and isolates any compromised archives. 

Here are the exact requirements for your script:
1. Find all compressed tar archives (files ending in `.tar.gz`) recursively within the directory `/home/user/backups`.
2. Analyze the contents of each archive without extracting them to disk (use compressed stream processing/listing).
3. Identify any archive that contains a file path with the literal substring `../`.
4. If an archive contains such a path, perform the following actions:
   a. Create a symbolic link to the vulnerable archive inside `/home/user/quarantine/` (you must create this directory first). The symlink should have the same base name as the target archive.
   b. Append a log entry to `/home/user/quarantine_log.txt` in the exact following format:
      `VULNERABLE: <absolute_path_to_archive> -> <suspicious_file_path>`
   c. If a single archive has multiple suspicious paths, only log the *first* one that appears in the archive's table of contents.
5. The script must be fully self-contained, executable, and written in Bash.
6. Once written, execute the script so that the `quarantine` directory and the `quarantine_log.txt` file are generated.

Note: Ensure your script correctly handles file paths and uses absolute paths for the symlink targets to avoid broken links.