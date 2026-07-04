You are a backup administrator tasked with migrating legacy log archives into a new, highly compressed, and unified format.

Over the past year, logs were archived using a proprietary internal tool. We have 50 backup files located in `/home/user/legacy_backups/` (named `backup_00.pck` to `backup_49.pck`). We no longer have the source code for the tool that created these, but we do have a stripped binary at `/app/pck_unpack` that can extract them.

If you run `/app/pck_unpack <file.pck>`, it will output the uncompressed contents of that file to `stdout`. 

The uncompressed stream consists of raw JSON lines. However, due to disk corruption, some of these log lines are damaged. 

Your objective is to write a Python script at `/home/user/archive_logs.py` that does the following:
1. Iterates through all `.pck` files in `/home/user/legacy_backups/`.
2. Uses `/app/pck_unpack` to stream their uncompressed contents.
3. Performs archive integrity verification by parsing each JSON line. A line is valid ONLY if it contains a `checksum` field that exactly matches the MD5 hash (represented as a hex string) of its `payload` field. Drop any invalid or corrupted lines.
4. Converts the valid JSON lines into a standard CSV format with the headers exactly as follows: `timestamp,severity,payload`.
5. Compresses the aggregated CSV data into a single GZIP archive at `/home/user/optimized_logs.csv.gz`.

**Important Compression Constraint:**
We are severely constrained on storage space for the new backup server. Your final `optimized_logs.csv.gz` file must be highly optimized. Standard compression of the raw stream will likely produce a file around 2.5 MB. You must implement a strategy within your Python script (such as sorting the rows by specific columns to group similar data) to maximize the dictionary compression efficiency of GZIP. 

The automated test will measure the file size of `/home/user/optimized_logs.csv.gz`. To pass, the final archive size must be strictly less than **1,200,000 bytes**.

Do not use external libraries outside the Python standard library. Shell commands and subprocesses are allowed.