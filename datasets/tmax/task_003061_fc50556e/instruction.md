I need you to help me organize a messy project dump directory located at `/home/user/project_dump`. Assets and logs have been mixed up, and I need to extract, transform, and organize specific data using a combination of shell commands and a Go script.

Here is what you need to do:

1. **Extract Hidden Binaries:** Some image files in `/home/user/project_dump` have been accidentally saved with incorrect extensions (like `.txt`, `.dat`, or no extension). Identify all files that are actually PNG images (by inspecting their binary headers/magic numbers). Move these files to `/home/user/assets/images/` and ensure they have a `.png` extension appended to their original filename (e.g., `data.dat` becomes `data.dat.png`).

2. **Metadata Search & Text Transformation:** Find all `.log` files in `/home/user/project_dump` that are larger than 100 bytes. Extract all lines from these files that contain the exact uppercase word "CRITICAL". While extracting, use `sed` or `awk` to redact any IPv4 addresses in those lines, replacing them exactly with the string `[REDACTED]`. Save this consolidated list of redacted critical lines to an intermediate file at `/home/user/consolidated_critical.txt`.

3. **File Chunking with Go:** Write and execute a Go script at `/home/user/split_logs.go`. This script must read `/home/user/consolidated_critical.txt` and split it into multiple smaller chunk files in the directory `/home/user/assets/logs/`. Each chunk file must contain exactly 15 lines (the final chunk may contain fewer if there is a remainder). Name the chunk files `critical_chunk_1.txt`, `critical_chunk_2.txt`, etc.

Make sure the destination directories (`/home/user/assets/images/` and `/home/user/assets/logs/`) exist before moving or writing files to them.