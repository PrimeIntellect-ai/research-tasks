You are acting as a storage administrator managing disk space on a central logging server. We are running out of space due to massive, verbose transaction logs coming from our storage nodes. 

Your task is to write a Python script at `/home/user/process_logs.py` and run it to transform these logs, saving disk space by retaining only the failed transactions, and then generate a verification manifest.

Here are the exact requirements:

1. **Input Data**: The original logs are located in `/home/user/raw_logs/`. There are multiple `.log` files. Each file contains a series of multi-line transaction records formatted exactly like this:
```
=== START TRANSACTION <ID> ===
Timestamp: <Date/Time>
Status: <SUCCESS|FAILED>
Details:
  <...multiple lines of arbitrary text...>
=== END TRANSACTION <ID> ===
```

2. **Parsing & Filtering**: Your Python script must read each `.log` file and parse the multi-line records. You must extract *only* the transactions where `Status: FAILED`. The extracted multi-line records must be kept exactly as they are (from the `=== START...` line to the `=== END...` line inclusive), including original whitespace and newlines.

3. **Atomic Writes**: To prevent data corruption in case the disk gets full during writing, the script must use atomic writes for the output. For each input file (e.g., `node1.log`), write the filtered records to a temporary file named `node1.log.tmp` inside `/home/user/processed_logs/`. Once the file is completely written and closed, atomically rename it to `node1.log` in the same directory. 

4. **Manifest and Checksums**: After all logs are processed and atomically renamed, your script must generate a manifest file at `/home/user/processed_logs/manifest.json`. This file must be a valid JSON dictionary mapping the final processed filename (e.g., `"node1.log"`) to its SHA256 hex digest.

Execute your script so that `/home/user/processed_logs/` is populated correctly. 

**Constraints:**
- Use standard Python libraries only.
- Do not modify the original files in `/home/user/raw_logs/`.
- Ensure `/home/user/processed_logs/` exists before writing.