You are acting as a Storage Administrator. We have a directory containing user-uploaded archives, and we need to process them while managing disk space and preventing security issues. 

Some users have been uploading archives that contain malicious "Zip Slip" paths (e.g., paths containing `../` or absolute paths like `/etc/passwd`) designed to overwrite system files when extracted. Additionally, many of the legacy text files inside these archives are in an older encoding, and we need everything standardized for our new storage backend.

Please write and execute a Python script to perform the following tasks:

1. **Input and Output Directories**:
   - Process all `.zip` and `.tar.gz` archives located in `/home/user/uploads`.
   - Extract valid files into `/home/user/processed/extracted`.
   
2. **Security & Integrity Check (Zip Slip prevention)**:
   - Inspect the paths of all files within each archive.
   - An archive is considered "malicious" if it contains ANY file with an absolute path (starting with `/`) or a path containing directory traversal sequences (`../` or `..\`).
   - If an archive is malicious, **do not extract any of its files**. Instead, delete the archive from `/home/user/uploads` to save disk space, and append its base filename to `/home/user/processed/deleted.log` (sort this log file alphabetically at the end).

3. **Safe Extraction & Character Encoding Conversion**:
   - For safe archives, extract all files to `/home/user/processed/extracted`, preserving the directory structure defined in the archive.
   - After extraction, find all files with the `.txt` extension. These legacy text files are currently encoded in `cp1252`. You must read them and overwrite them in `utf-8` encoding. Non-text files (any file without a `.txt` extension) must remain completely untouched binary-wise.

4. **Manifest and Checksum Generation**:
   - Generate a manifest file at `/home/user/processed/manifest.json`.
   - The manifest must be a JSON object where the keys are the relative file paths (relative to `/home/user/processed/extracted/`) and the values are the SHA-256 hex digests of the final extracted (and potentially utf-8 converted) files.

Make sure the final output directories exist before writing to them. You may use standard Python libraries (`zipfile`, `tarfile`, `hashlib`, `json`, `os`, `shutil`, etc.) to accomplish this. Do not rely on external tools like `unzip` or `tar` CLI commands to extract, as we need strict programmatic control over the extraction paths to prevent Zip Slip.