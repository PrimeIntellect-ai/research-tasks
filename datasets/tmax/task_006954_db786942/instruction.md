You are a developer tasked with organizing and filtering a large collection of project log files. 

You have a directory at `/home/user/raw_logs` containing several gzipped log files (e.g., `server_alpha.log.gz`, `server_beta.log.gz`). Because these files can theoretically be larger than available memory, you need to process them efficiently and safely.

Write a Python script at `/home/user/extract_critical.py` that does the following:
1. Iterates through all `.log.gz` files in `/home/user/raw_logs` in alphabetical order by filename.
2. Uses compressed stream processing to read each file line-by-line (do not load the entire file into memory at once).
3. Extracts any line that contains the exact substring `[CRITICAL]`.
4. Writes the combined extracted lines to a final destination file at `/home/user/critical_summary.log`.
5. Guarantees that the final output file is never seen in a partially written state. You MUST use an atomic write pattern: write all the filtered lines into a temporary file first (using Python's `tempfile` module or similar), flush and close it, and then atomically rename/replace it to `/home/user/critical_summary.log`.

Once you have written the script, execute it so that `/home/user/critical_summary.log` is generated.