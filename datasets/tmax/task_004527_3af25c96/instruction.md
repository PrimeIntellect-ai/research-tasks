You are acting as a backup administrator. We have a legacy nested archive containing old server logs that need to be extracted, transformed, filtered, and repackaged for our modern log analysis system.

The legacy archive is located at `/home/user/legacy_logs.tar`.

Inside this tarball, there are several zip files (one for each server). Inside those zip files are gzip-compressed log files.
The uncompressed log files are pipe-separated values (PSV) with the following columns (no header row):
`TIMESTAMP|LEVEL|MODULE|MESSAGE`

Your task is to write a Python script (and use standard Linux shell commands as needed) to do the following:
1. Recursively extract all logs from the nested archive (`.tar` -> `.zip` -> `.gz`).
2. Read the extracted log files.
3. Filter the logs to keep ONLY the lines where the `LEVEL` is exactly `ERROR`.
4. Convert these filtered lines into a JSON array of objects. The JSON keys must be `timestamp`, `level`, `module`, and `message`.
5. Save the JSON output for each original log file as a new file named `<original_filename>_errors.json`. For example, if the original uncompressed file was `app_1.log`, the output should be `app_1.log_errors.json`. All JSON files should be saved in a new directory: `/home/user/processed_logs/`.
6. Finally, package the `/home/user/processed_logs/` directory into a multi-part ZIP archive located at `/home/user/archive_out/error_logs.zip`. The archive must be split into chunks of exactly 20 kilobytes (20k). You can use standard bash tools like `zip` for this final step.

Ensure that:
- You create the output directories `/home/user/processed_logs/` and `/home/user/archive_out/` before writing to them.
- The final output is specifically a multi-part zip file (e.g., creating `error_logs.zip`, `error_logs.z01`, etc., depending on the tool used, standard `zip -s 20k` behavior is expected).