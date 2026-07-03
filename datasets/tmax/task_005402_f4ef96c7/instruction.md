You are a storage administrator managing a legacy Linux server. Disk space is critically low due to massive, uncompressed proprietary binary log files stored in a tarball. 

We need to extract these logs, parse them, filter out the noise, and re-compress them as efficiently as possible to free up disk space.

Here is your task:
1. Extract the contents of `/home/user/raw_logs.tar`. It contains several proprietary binary log files (`.binlog`).
2. There is a stripped, legacy utility located at `/app/bin_to_json` that can parse these binary log files. If you run `/app/bin_to_json <input_file>`, it outputs newline-delimited JSON records to `stdout`.
3. Write and execute a Python script `/home/user/compact_logs.py` that automates this process:
   - Iterates over all extracted `.binlog` files.
   - Uses the `/app/bin_to_json` utility to parse them into JSON.
   - Filters out any JSON record where the `"level"` key equals `"DEBUG"`.
   - Writes all remaining JSON records into a single, highly compressed GZIP file at `/home/user/filtered.json.gz`.
   - You must maximize the compression ratio. Use the highest compression level available in your GZIP implementation to ensure the resulting file takes up the absolute minimum disk space possible.

Ensure your Python script runs successfully and generates the final `/home/user/filtered.json.gz` file. The automated verification system will check the final file size against a strict metric threshold to ensure optimal space savings.