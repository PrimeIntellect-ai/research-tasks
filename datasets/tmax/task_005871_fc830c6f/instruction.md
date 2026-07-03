You are an AI assistant helping a backup administrator create a robust incremental backup script. 

The administrator has a data directory at `/home/user/data_source`. This directory contains a mix of text files, large binary data files (`.dat`), and complex subdirectories. Unfortunately, some users have created symlinks within this directory that form infinite loops.

Your task is to write and execute a Python script at `/home/user/perform_backup.py` that performs an incremental backup of `/home/user/data_source` to `/home/user/backup_dest/inc_01`.

Here are the specific requirements for your script:

1. **Incremental Logic**:
   - An old manifest exists at `/home/user/old_manifest.json`. It is a JSON dictionary mapping file paths (relative to `/home/user/data_source`) to their SHA256 hashes.
   - Your script must compute the SHA256 hash of every regular file in `/home/user/data_source`.
   - If a file is NOT in the old manifest, or its hash differs from the old manifest, it must be copied to `/home/user/backup_dest/inc_01/` (preserving its relative directory structure).
   - If a file has not changed, do NOT copy it.

2. **Symlink Navigation & Loop Handling**:
   - The script must follow symlinks to discover files.
   - You must detect and prevent infinite symlink loops.
   - Whenever a symlink loop is detected (e.g., encountering a directory path that has already been visited in the current traversal branch), you must skip it and append the absolute path of the offending symlink to `/home/user/symlink_warnings.log`. Each path should be on a new line.

3. **Memory-Mapped I/O**:
   - For all files ending in `.dat`, you must use Python's `mmap` module to read the file contents when computing the SHA256 hash.

4. **New Manifest**:
   - After traversal, write a new manifest to `/home/user/backup_dest/manifest_01.json`.
   - The format must be identical to the old manifest: a flat JSON object where keys are the relative file paths (e.g., `dirA/file.txt`) and values are the SHA256 hash strings of the current files. Do not include directories or skipped symlinks in the manifest keys.

Ensure your script is self-contained, creates the destination directories if they don't exist, and runs successfully. Once you have written the script, execute it so the backup and manifests are generated.