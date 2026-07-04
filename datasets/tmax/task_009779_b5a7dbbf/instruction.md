You are a storage administrator managing disk space and handling historical system log backups. A legacy backup system has dumped a series of split tar archives into `/home/user/storage_dumps`. You suspect some of these archives were created by a compromised system and contain "Zip Slip" payloads (malicious paths designed to overwrite files outside the extraction directory, such as `../../../etc/passwd` or `/root/ssh_keys`). 

Your task is to create a Rust program that safely processes these archives, detects the malicious paths, and extracts actionable disk-space alerts from the safe multi-line logs.

Write and execute a Rust project at `/home/user/archive_processor`. Your Rust program must perform the following pipeline:

1. **File Merging & Traversal**: 
   Recursively traverse `/home/user/storage_dumps` to find all split archive parts. The files are named with the pattern `[archive_name].tar.part[N]` (e.g., `backupA.tar.part1`, `backupA.tar.part2`). Merge these parts in numerical order to reconstruct the complete `.tar` files in `/home/user/merged_archives/` (you must create this directory).

2. **Archive Integrity & Security Verification**:
   Process each merged `.tar` file. Do NOT blindly extract the archive to the filesystem. Instead, inspect the path of each entry in the archive.
   - A path is considered **unsafe** (Zip Slip payload) if it is an absolute path (starts with `/`) or contains `..` components that would resolve outside of a hypothetical extraction root.
   - Write every unsafe path exactly as it appears in the archive metadata to `/home/user/unsafe_paths.log` (one path per line, sorted alphabetically).
   - Do NOT extract unsafe files.

3. **Safe Extraction**:
   For entries that are safe and have a `.log` extension, read their contents into memory or extract them to `/home/user/extracted_logs/`.

4. **Multi-line Log Parsing**:
   The safe `.log` files contain multi-line log records. Each record is separated by a line containing exactly `---`.
   The record fields are formatted as `Key: Value`, possibly spanning multiple lines for the Message.
   Example:
   ```
   ---
   Timestamp: 2023-10-01T10:05:00Z
   Severity: ERROR
   Message: Disk space critical on /dev/sda1
   Please clean up old backups.
   ---
   ```
   Parse these records and find all records where the `Severity` is exactly `ERROR` AND the `Message` text contains the exact phrase `Disk space critical`.
   
5. **Output**:
   Write the `Timestamp` values of all matching critical disk space errors to `/home/user/critical_disk_errors.txt` (one timestamp per line, sorted chronologically).

You may use standard external crates like `tar` or `flate2` by configuring your `Cargo.toml`. When your code is ready, compile and run it to produce the final `unsafe_paths.log` and `critical_disk_errors.txt` files.