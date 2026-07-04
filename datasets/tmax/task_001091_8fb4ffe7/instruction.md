You are acting as a backup administrator. We have a proprietary backup system that creates custom archive files with a `.bkp` extension. 

You need to write a Rust program to audit these backup files. The backups are stored in the directory `/home/user/backups/`. Each backup file contains a binary header followed by a large data payload. You must extract metadata from these headers without loading the entire payload into memory (using streaming or memory-mapped I/O to read just the start of the file).

**The `.bkp` Binary Format:**
1. Magic Bytes (4 bytes): Exact ASCII characters `BKP1`
2. Creation Timestamp (8 bytes): Unsigned 64-bit integer, little-endian (UNIX epoch seconds)
3. Filename Length (2 bytes): Unsigned 16-bit integer, little-endian
4. Original Filename: UTF-8 string of the length specified in the previous field
5. Payload: Raw data (variable length, to be ignored)

Additionally, there is an inventory file located at `/home/user/inventory.csv` with the following columns:
`original_filename,retention_days`

**Your Goal:**
Write and execute a Rust program (e.g., in `/home/user/audit_project`) that:
1. Parses `/home/user/inventory.csv` to map original filenames to their retention days.
2. Iterates over all `.bkp` files in `/home/user/backups/`.
3. Reads and extracts the metadata from the binary header of each `.bkp` file.
4. Calculates the `expiration_timestamp` for each file. This is the file's Creation Timestamp plus the retention period in seconds (retention_days * 86400). If an original filename from a `.bkp` file is NOT found in the CSV, assume a default retention of `30` days.
5. Outputs a formatted JSON array to `/home/user/audit_report.json`.

**JSON Output Format:**
The output file `/home/user/audit_report.json` must contain a single JSON array containing objects with the following exact keys (sorted by `archive_filename` alphabetically):
```json
[
  {
    "archive_filename": "data_A.bkp",
    "original_filename": "database_prod.db",
    "creation_timestamp": 1700000000,
    "expiration_timestamp": 1707776000
  }
]
```

Please complete the task by creating the Rust project, writing the code, running it, and ensuring `/home/user/audit_report.json` is generated correctly.