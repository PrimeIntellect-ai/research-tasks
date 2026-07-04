You are tasked with helping a developer organize and parse a heavily fragmented set of project logs. Due to a broken log rotation script, the application's logs have been scattered across deeply nested subdirectories inside `/home/user/project_logs`. Furthermore, the application occasionally writes multi-line error messages that break standard line-by-line grep analysis.

Your goal is to write and execute a Bash script (using standard tools like `awk`, `sed`, `find`, etc.) that processes these files using efficient streaming techniques, transforming the data into a single, structured file. 

Here are the requirements:
1. Traverse `/home/user/project_logs` to find all files ending in `.log`.
2. Process the contents of these files to extract only the `[ERROR]` and `[CRITICAL]` log entries.
3. Handle multi-line log entries: Any line that does *not* start with a `[` character is a continuation of the previous log entry. You must join these continuation lines to the main entry line, replacing the newline characters with a single tab character (`\t`).
4. Transform the timestamp: The original logs have timestamps in the format `[YYYY-MM-DD HH:MM:SS]`. You must reformat this to `YYYY/MM/DD-HH:MM:SS` (removing the brackets and replacing the space with a hyphen).
5. The extracted and formatted lines must be formatted as tab-separated values (TSV) with exactly three columns: 
   `TIMESTAMP<TAB>LEVEL<TAB>MESSAGE_CONTENT`
   (Note: `LEVEL` should just be `ERROR` or `CRITICAL` without the brackets. `MESSAGE_CONTENT` includes the joined multi-line strings).
6. Consolidate all processed error/critical logs from all files, sort them chronologically by the new timestamp (oldest first), and save the final output to `/home/user/organized_errors.tsv`.

Do not load all files into memory at once; use streaming I/O (e.g., `find` piped to `awk`/`sed` or similar stream processors) to handle the transformation. Ensure your solution is self-contained and leaves the final organized file at `/home/user/organized_errors.tsv`.