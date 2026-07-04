You are assisting a storage administrator in managing and securing user uploads. Users frequently upload `.tar.gz` archives to the `/home/user/incoming` directory. However, some of these archives are malicious and contain "zip slip" payloads—files with absolute paths (e.g., `/etc/passwd`) or directory traversal sequences (e.g., `../.ssh/id_rsa`) that could overwrite sensitive files if carelessly extracted.

Your task is to write a Python script at `/home/user/sanitize.py` that does the following:
1. Iterates over all `.tar.gz` files in `/home/user/incoming/`.
2. Reads each archive as a compressed stream (do **not** extract the archives to disk).
3. Inspects the paths of the files inside the archive. Any file entry whose path is absolute (starts with `/`) or contains directory traversal components (contains `../` or `..` as a path segment) must be discarded.
4. Writes the safe files into a new `.tar.gz` archive in the `/home/user/processed/` directory.
5. The new filename must follow a specific bulk renaming convention: `<original_basename>_safe_<total_uncompressed_bytes>.tar.gz`. For example, if the original file was `upload1.tar.gz` and the safe files inside it have a combined uncompressed size of 1024 bytes, the new file should be `/home/user/processed/upload1_safe_1024.tar.gz`.

Run your script to process the files currently in the `/home/user/incoming/` directory.

**Environment details:**
- Incoming directory: `/home/user/incoming/`
- Output directory: `/home/user/processed/` (create this if it doesn't exist)
- Python 3 is available. You may use standard library modules like `tarfile` and `os`.