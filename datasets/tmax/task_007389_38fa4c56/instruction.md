You are an AI assistant helping a configuration manager secure and process system updates. 

A new configuration patch has been delivered to `/home/user/config_update/patch.zip`. However, we suspect this archive may have been tampered with to include a "Zip Slip" vulnerability, containing malicious paths (like `../` or absolute paths) designed to overwrite files outside the intended extraction directory.

We also maintain a custom Write-Ahead Log (WAL) of our configurations located at `/home/user/config_update/system.wal`. The WAL records the last known state of our configs in a domain-specific pipe-delimited format:
`ENTRY|<timestamp>|<filename>|<md5_hash>`

Your task is to write and execute a Python script at `/home/user/config_update/process_patch.py` that performs the following:
1. **Safely Extract (Zip Slip Protection)**: Programmatically extract `patch.zip` into the directory `/home/user/config_update/safe_extract/`. You must strictly prevent any directory traversal. If an entry's normalized absolute extraction path does not start with the absolute path of the `safe_extract` directory, it must be completely ignored.
2. **Parse the WAL**: Read `system.wal` to determine the last known MD5 hash for each filename. (Assume filenames in the WAL correspond to the base names of the extracted files).
3. **Differential Analysis**: For every file successfully and safely extracted, calculate its current MD5 hash. Compare this to the hash recorded in the WAL. If the extracted file's hash differs from the WAL, or if the file does not exist in the WAL at all, it is considered a "changed" or "new" file.
4. **Generate Backup List**: Write the absolute paths of all changed or new files (from the `safe_extract` directory) into `/home/user/config_update/differential_backup.list`, with one path per line, sorted alphabetically.

Ensure your script handles everything end-to-end. Once you have written the script, run it so that the final `differential_backup.list` is generated.