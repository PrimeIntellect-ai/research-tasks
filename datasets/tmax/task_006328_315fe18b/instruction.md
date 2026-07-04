You are acting as a backup administrator. You need to automate the extraction and filtering of critical log events from a backup drop directory. 

We have a directory at `/home/user/backup_drop/` where various systems dump their log files. Some are gzipped archives, some are plain text, and some are mislabeled or corrupted files.

Your task is to write a Python script at `/home/user/process_backups.py` that performs the following steps:

1. **File Watch/State Detection:** 
   The script should only process files in `/home/user/backup_drop/` that have a modification time (`mtime`) strictly strictly greater than the timestamp stored in `/home/user/last_run.stamp` (this file contains a single Unix epoch timestamp as a float or int). 

2. **Binary Header Extraction:**
   Do not trust file extensions. For each eligible file, read the first 2 bytes to determine its true format:
   - If the first 2 bytes are `\x1f\x8b`, treat it as a gzip file.
   - If the first 2 bytes are `\x2d\x2d` (which corresponds to `--`), treat it as a plain text log file.
   - Skip any files that do not match these magic signatures.

3. **Stream Redirection, Piping, and Text Transformation:**
   For valid files, you must extract the contents and filter them by invoking a shell pipeline via Python's `subprocess` module. 
   - For gzip files, the pipeline should start with `zcat`.
   - For plain text files, the pipeline should start with `cat`.
   - The stream must be piped into `awk` to filter and only output lines containing the word `CRITICAL`.
   - The stream must then be piped into `sed` to anonymize all IPv4 addresses (e.g., `192.168.1.50`), replacing them entirely with the string `[REDACTED]`.

4. **Archiving Output:**
   Append the final processed and redacted lines to `/home/user/critical_archive.txt`.

5. **State Update:**
   After processing all eligible files, update `/home/user/last_run.stamp` with the current system time so subsequent runs don't re-process the same files.

Execute your script once to process the current backlog. We will verify the contents of `/home/user/critical_archive.txt`. Ensure your Python script is executable or can be run via `python3 /home/user/process_backups.py`.