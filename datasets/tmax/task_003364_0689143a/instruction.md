You are acting as a backup administrator dealing with a legacy system. You need to write a Rust tool to safely archive application snapshot data based on configuration, log status, and binary integrity. 

Your task is to create a Rust project in `/home/user/archiver` and write a program that performs the following steps:

1. **Configuration Interpretation:**
   Read the JSON configuration file at `/home/user/backup_config.json`. It contains the following keys:
   - `source_dir`: Directory containing the binary snapshots.
   - `archive_dir`: The destination directory where valid snapshots should be archived.
   - `expected_magic`: An array of 8 integers representing the expected binary header (magic bytes) of a valid snapshot.

2. **Multi-line Log Parsing:**
   Read the synchronization log file at `/home/user/data/sync.log`. The log consists of multi-line blocks formatted like this:
   ```
   [TRANSACTION]
   ID: 101
   Status: SUCCESS
   File: snap_101.bin
   [/TRANSACTION]
   ```
   Parse this file to identify the filenames (e.g., `snap_101.bin`) of all transactions where `Status: SUCCESS`. Ignore transactions with any other status.

3. **Memory-Mapped Binary Header Extraction:**
   For each "SUCCESS" file identified in the log, open the corresponding file in the `source_dir`. 
   Using **memory-mapped I/O** (e.g., the `memmap2` crate), map the file and extract the first 8 bytes (the header).
   Verify that these 8 bytes exactly match the `expected_magic` array from the configuration file.

4. **Hard Link Management:**
   If a file is marked SUCCESS in the log *and* its binary header matches the magic bytes, create a **hard link** to this file in the `archive_dir` (creating the `archive_dir` if it does not exist). The hard-linked file must have the same name as the original.

5. **Reporting:**
   Create a report file at `/home/user/archive_report.txt`. This file should contain a plain-text list of the filenames that were successfully archived (hard-linked), one per line, sorted alphabetically.

**Constraints:**
- You must use Rust to implement this logic. Feel free to use `cargo new /home/user/archiver` and add necessary dependencies like `serde`, `serde_json`, and `memmap2`.
- Execute your Rust program so the final state is achieved.
- Do not move or copy the files; they *must* be hard-linked to save space.