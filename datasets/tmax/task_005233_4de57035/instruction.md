You are an AI assistant helping a backup administrator archive critical production logs. 

There is a directory structure at `/home/user/raw_logs` that contains mixed environments (`prod`, `dev`, `staging`) and applications. Inside these directories are various compressed log files (`.log.gz`).

Your task is to:
1. Recursively find all `.log.gz` files that are located inside any directory named exactly `prod` (e.g., `/home/user/raw_logs/app1/prod/sys.log.gz`). Ignore logs in `dev` or `staging`.
2. Process the contents of these `prod` log files on-the-fly without permanently extracting them to disk.
3. During processing, perform the following text transformations:
   - Remove any log line that contains the word `DEBUG`.
   - Redact IPv4 addresses: Replace matches of the pattern `IP: <any-valid-or-invalid-IPv4>` (e.g., `IP: 192.168.1.50`) with `IP: REDACTED`.
4. Combine the transformed output from all processed files into a single stream. The order in which files are concatenated does not matter.
5. Compress the combined stream using `gzip`.
6. Split the resulting compressed stream into chunks of exactly 50 Kilobytes (50KB = 50 * 1024 bytes).
7. Save the split chunks in the directory `/home/user/archive/` (which you must create). Name the chunks using the prefix `prod_logs.gz.part-` followed by a two-letter alphabetical suffix (e.g., `prod_logs.gz.part-aa`, `prod_logs.gz.part-ab`, etc.).

Ensure you clean up any temporary files used during processing. The final state should just have the directory `/home/user/archive/` containing only the chunked files.