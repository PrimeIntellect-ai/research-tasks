You are a storage administrator managing a mock storage pool on a Linux server. Over time, automated backup systems have dumped numerous archive files into the storage pool, some of which are corrupted or incomplete. You need to identify old, large archives and verify their integrity to free up disk space safely.

Your task is to write a Python script at `/home/user/verify_storage.py` that performs the following operations:

1. **Traverse and Search**: Recursively search the directory `/home/user/data_mount` for all archive files (specifically ending in `.zip` and `.tar.gz`).
2. **Metadata Filtering**: Filter the discovered archives based on file metadata. You must only process archives that:
   - Are larger than 50 KB (51,200 bytes) in size.
   - Have a modification time (mtime) strictly older than 30 days from the current system time.
3. **Path Manipulation**: Some of the files might be symlinks. You must resolve all symlinks to their absolute canonical target paths before checking their size, mtime, and integrity. Ensure you do not process the exact same physical file twice if multiple symlinks point to it.
4. **Archive Integrity Verification**: For each file that passes the metadata filter, verify its integrity.
   - For `.zip` files, check if they can be read without CRC or structural errors.
   - For `.tar.gz` files, check if the gzip compression and tar structure are intact.
5. **Output**: 
   - Write the absolute, resolved paths of all **corrupted** (or invalid) archives that met the filter criteria to `/home/user/corrupt_backups.txt`.
   - Write the absolute, resolved paths of all **valid** archives that met the filter criteria to `/home/user/valid_backups.txt`.
   - Both output files must have exactly one absolute path per line and must be sorted alphabetically.

Do not delete any files; only generate the report files. You can use standard Python libraries (like `os`, `Pathlib`, `zipfile`, `tarfile`, `time`) or call out to standard CLI utilities via `subprocess`.

Once your script is written, execute it to generate `/home/user/corrupt_backups.txt` and `/home/user/valid_backups.txt`.