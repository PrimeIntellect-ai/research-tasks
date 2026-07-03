You are a storage administrator tasked with managing disk space and updating log archives. We have a set of legacy compressed log files that use an outdated naming convention and a custom, bulky text format. To optimize storage and prepare the logs for our modern analytics pipeline, you need to consolidate, convert, and rename these archives.

Here is the current state of the system:
- A configuration file exists at `/home/user/service_mapping.conf`. It contains mappings of old application names to new service names, in the format `old_name=new_service_name`.
- A directory `/home/user/legacy_logs/` contains several gzipped log files named like `app_<old_name>_archive.log.gz`.
- Inside these compressed files, the text logs are formatted as follows: `[LEVEL] YYYY-MM-DD message body here`

Your objective is to:
1. Write a Rust program at `/home/user/converter.rs` (and compile it to `/home/user/converter`) that reads the custom log format from Standard Input (stdin) and outputs JSONLines (NDJSON) to Standard Output (stdout). Each JSON object should have the keys: `"level"`, `"date"`, and `"message"`.
2. Use shell commands (bash, awk, sed, etc.) combined with your compiled Rust program to process every `.log.gz` file in `/home/user/legacy_logs/`.
3. For each file:
   - Stream the decompressed contents through your Rust converter.
   - Compress the JSON output back into gzip format.
   - Save the new file in `/home/user/processed_logs/` (you will need to create this directory).
   - Rename the file using the mapping from `/home/user/service_mapping.conf`. The new filename should be `<new_service_name>_archive.json.gz`.
4. After successfully processing the files, delete the entire `/home/user/legacy_logs/` directory to free up disk space.

Example input line: `[ERROR] 2023-10-12 Database connection failed`
Example output line: `{"level":"ERROR","date":"2023-10-12","message":"Database connection failed"}`

Ensure your Rust program gracefully ignores any lines that do not strictly match the `[LEVEL] DATE MESSAGE` pattern.