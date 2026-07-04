You are acting as a backup administrator. We have a set of raw, unredacted log files from our web servers that need to be safely processed, sanitized, and renamed before they are moved to long-term cold storage.

There is a directory at `/home/user/raw_backups` containing 50 log files with inconsistent, chaotic names (e.g., `web_node_A_log_8f32a.dat`). Each file is roughly 1MB of binary/text data. 

Your task is to write a Rust program in `/home/user/archiver/` (you will need to initialize the Cargo project) that performs the following steps:

1. **Bulk File Renaming**: Read all files in `/home/user/raw_backups`. Sort the original filenames alphabetically. You must map these files to a new standardized naming scheme: `archive_001.dat`, `archive_002.dat`, ..., `archive_050.dat` based on their sorted order.
2. **Streaming / Memory-Mapped I/O for Sanitization**: Process each file to redact sensitive tokens. Find every instance of the exact 21-character string `SECRET_TOKEN:`, immediately followed by 8 alphanumeric characters (e.g., `SECRET_TOKEN:A1B2C3D4`). You must replace the entire 21-character block with exactly `REDACTED_KEY:00000000`. Because these files are large, you must use either efficient chunked streaming or Memory-Mapped I/O (`memmap2`) to process them quickly.
3. **Atomic Writes and Temp File Management**: You must ensure that if the process is interrupted, no corrupted files are left in the destination directory (`/home/user/processed_backups/`). For each file, write the sanitized output to a temporary file in `/home/user/processed_backups/` (e.g., `.tmp_archive_001.dat`), and once writing/flushing is completely finished, atomically rename it to its final name (e.g., `archive_001.dat`).
4. **Audit Log**: Your Rust program must generate a log file at `/home/user/audit_log.txt`. Each line must contain the exact mapping of the rename operation in this format:
   `[ORIGINAL_FILENAME] -> [NEW_FILENAME]`
   (e.g., `node_01_xyz.dat -> archive_001.dat`).

**Instructions:**
- Create the Rust project.
- Write the code, add dependencies as needed (e.g., `regex`, `memmap2`, `tempfile`).
- Compile and run your application.
- Ensure the destination directory `/home/user/processed_backups/` is created by your program if it doesn't exist.
- Leave the original files in `/home/user/raw_backups` untouched.