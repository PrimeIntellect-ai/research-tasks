You are acting as a configuration manager. We have a directory of automated configuration backup archives located at `/home/user/config_archives/`. These archives contain multi-line changelog files named `changelog.txt`. 

Your goal is to parse these logs to generate a final deployment manifest of configuration files modified by a specific automated service account.

Follow these steps exactly to complete the task:

1. **Archive Integrity & Extraction**: 
   Iterate through all `.tar.gz` files in `/home/user/config_archives/`. One or more of these archives may be corrupted. You must programmatically verify their integrity. Extract the `changelog.txt` files *only* from the valid archives into `/home/user/extracted_logs/`. Rename each extracted file to match its source archive's base name (e.g., the log from `batch_01.tar.gz` should be saved as `/home/user/extracted_logs/batch_01.txt`).

2. **Text Transformation**:
   The logging system injects legacy debug lines that break standard parsing. Using `sed` or `awk`, process all the extracted `.txt` files in `/home/user/extracted_logs/` to remove any line that begins exactly with the string `!! DEBUG`. Overwrite the files with the cleaned output.

3. **Multi-line Log Parsing**:
   Write a Python script at `/home/user/parser.py` that reads the cleaned log files in alphabetical order (e.g., `batch_01.txt` before `batch_02.txt`). 
   The log files use a multi-line format like this:
   ```
   [TRANSACTION]
   User: <username>
   Timestamp: <epoch>
   Modified_Files:
    - <filepath>|<sha1_hash>
    - <filepath>|<sha1_hash>
   [END]
   ```
   Your script must extract all file paths and their associated hashes for transactions where the `User` is exactly `svc_deploy_ops`. 
   If a file is modified multiple times across different transactions or different log files, keep only the *latest* hash (based on the alphabetical processing order of the log files, and top-to-bottom order within a file).

4. **Manifest Generation**:
   The Python script must output the final deduplicated dictionary of files and their latest hashes as a strictly formatted JSON file at `/home/user/deploy_manifest.json`. The JSON should be a flat key-value object: `{"/path/to/file": "hash", ...}`.

5. **Checksum Generation**:
   Finally, generate a SHA256 checksum of `/home/user/deploy_manifest.json` and save the output to `/home/user/manifest_checksum.txt` in the standard `sha256sum` format.

Ensure all file paths and names match the instructions exactly.