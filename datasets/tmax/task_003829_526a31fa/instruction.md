You are assisting a storage administrator who is managing disk space. A custom Rust-based backup service recently failed, filling up the disk with a corrupted backup archive before crashing. We suspect it followed a symlink into an infinite loop.

The corrupted backup archive is located at `/home/user/backups/latest.bak`.
The directory that was being backed up is `/home/user/data/`.

Your task is to:
1. Find the symlink inside `/home/user/data/` (or its subdirectories) that points to an ancestor directory, creating an infinite loop. Delete this symlink to prevent future issues.
2. The backup archive is a custom binary format. The first 4 bytes are a magic number (ASCII string). The next 4 bytes are a little-endian unsigned 32-bit integer representing the length of the first file path attempted for backup. The next bytes (matching the length) are the ASCII string of that file path. 
3. Write a Rust program at `/home/user/parse_backup.rs` that opens `/home/user/backups/latest.bak`, extracts the file path from the binary header as described above, and prints ONLY the extracted file path to stdout.
4. Compile your Rust program and run it, redirecting its output to `/home/user/report.txt`.

Ensure that:
- The recursive symlink is completely removed.
- `/home/user/report.txt` contains exactly the extracted path and nothing else.