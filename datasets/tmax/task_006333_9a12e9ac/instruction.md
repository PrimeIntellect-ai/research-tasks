You are a backup administrator tasked with archiving specific log files from a production directory into a secure backup archive. 

Write a Python script at `/home/user/archive_logs.py` that performs the following steps:
1. **Metadata-based File Search:** Search the directory `/home/user/logs_source` for all files with the `.log` extension that have a file size strictly greater than 10240 bytes (10 KB).
2. **Bulk Renaming and Staging:** Copy these identified files into `/home/user/staging`. As you copy them, rename each file by appending its last modification date (in `YYYYMMDD` format) before the extension. For example, if `server.log` was last modified on October 5, 2023, it should be copied as `server_20231005.log`.
3. **Manifest and Checksum Generation:** Calculate the SHA-256 checksum for each of the renamed `.log` files in the staging directory.
4. **Atomic Write:** Create a manifest file containing these checksums. To ensure the manifest is not read while incomplete, you must write the checksums to a temporary file first, and then atomically move (rename) it to `/home/user/staging/manifest.sha256`. The format of each line in the manifest should be `<sha256_hash>  <filename>` (two spaces between hash and filename, and the filename should just be the base name of the file).
5. **Archiving:** Create a gzip-compressed tar archive named `/home/user/backups/logs_archive.tar.gz` that contains all the files in `/home/user/staging` (the renamed log files and `manifest.sha256`). The files should be at the root of the archive (do not include the `staging/` directory path inside the tarball).

**Constraints & Details:**
- Execute the Python script once you have written it.
- Ensure the `/home/user/backups` directory exists (create it if necessary).
- The checksums in the manifest must be lowercase.
- Only include the base filename in the manifest (e.g., `app_20231004.log`), not the full path.