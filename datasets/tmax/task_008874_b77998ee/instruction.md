You are acting as a storage administrator managing disk space and backup archives. We have a system that receives backup archives (ZIP format) from various external sources. We need to ensure these archives are safely processed, as we suspect some might be maliciously crafted to overwrite system files outside the extraction directory (a vulnerability known as "Zip Slip").

Your task has three parts:

1. **Text Transformation**:
   There is a configuration file located at `/home/user/backup_config.txt` that incorrectly points to an old path. Use a command-line text editor or stream editor (like `sed` or `awk`) to replace all instances of `/var/old_backups` with `/home/user/backups` directly in the file.

2. **Safe Extraction Script**:
   Write a Python script located at `/home/user/extract_safe.py` that does the following:
   - Reads the directory path from `/home/user/backup_config.txt`.
   - Iterates over all `.zip` files in that directory.
   - For each file, the script must obtain an exclusive, non-blocking file lock on the ZIP file using the `fcntl` module (to ensure we aren't reading an archive while another process is writing it). If it cannot acquire the lock, it should skip the file.
   - Without extracting the file yet, inspect the paths of the files inside the archive. An archive is considered "vulnerable" if any file path inside it starts with `/` (absolute path) or contains `../` (parent directory traversal).
   - If the archive is vulnerable, DO NOT extract it. Append the base filename (e.g., `archive.zip`) to `/home/user/vulnerable_archives.log`.
   - If the archive is safe, extract its contents to `/home/user/extracted/` and append the base filename to `/home/user/safe_archives.log`.
   - Release the lock after processing each file.

3. **Execution**:
   Run your script so that the logs and extracted files are generated.

Ensure that the output logs (`vulnerable_archives.log` and `safe_archives.log`) contain ONLY the base filenames of the processed zip files, one per line, sorted alphabetically.