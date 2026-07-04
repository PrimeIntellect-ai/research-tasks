You are a storage administrator managing disk space on a Linux server. A legacy application generates multiple large log files in `/home/user/data/logs/`. You need to archive these logs to save space, but the legacy application will crash if the log file paths completely disappear.

Write a Python script at `/home/user/archive_logs.py` and run it to perform the following operations:

1. **Archive Creation**: Find all `.log` files in `/home/user/data/logs/` and package them into a single compressed `tar.gz` archive in memory or a temporary location.
2. **File Chunking and Atomic Writes**: Split the resulting `tar.gz` archive into chunks of exactly 1 MB (1,048,576 bytes), except for the last chunk which may be smaller. 
   - Write these chunks to `/home/user/data/archive/` with the naming convention `chunk_000.dat`, `chunk_001.dat`, `chunk_002.dat`, etc.
   - **Crucial**: To prevent partial reads by other aggressive backup processes, you *must* write each chunk atomically. Specifically, write the chunk data to a temporary file (e.g., ending in `.tmp`) in the archive directory, and then rename it to the final `.dat` filename using an atomic filesystem operation.
3. **Symbolic Link Management**: For every original `.log` file in `/home/user/data/logs/`, delete the file and replace it with a symbolic link of the exact same name. This symbolic link must point to `/home/user/data/offline_placeholder.txt`.

Before running your script, ensure you understand the requirements. The automated test will verify that the chunks are correctly sized, the original files are now symlinks to the placeholder, and the reconstructed chunks form a valid tarball containing the original files.