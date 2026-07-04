You are tasked with building a secure configuration manager script in Python that processes incoming configuration updates from an archive while protecting against "Zip Slip" directory traversal vulnerabilities. 

Your goal is to write a Python script at `/home/user/config_manager.py` and then run it to process an incoming update archive located at `/home/user/incoming/updates.zip`. 

Here are the detailed requirements for `config_manager.py`:

1. **Extraction and Zip Slip Protection**:
   - The script must take two arguments: the path to the zip file, and the target extraction directory (`/home/user/app_configs`).
   - It must iterate through the files in the zip archive.
   - For each file, it must resolve the final absolute extraction path. If the resolved path falls outside the absolute path of the target extraction directory (e.g., due to `../` in the archive's file paths), the file **must not** be extracted.
   - Any malicious/unsafe file path found in the zip must be appended to `/home/user/rejected_updates.log`, with one original archive file path per line.
   - Safe files should be extracted to the target directory, preserving their directory structure (if any) within the target.

2. **Configuration Parsing and Ledger Application**:
   - All safe files extracted will be text files containing configuration properties in a simple `key=value` format (one per line). Ignore empty lines.
   - For every safe file extracted, the script must read its contents and append an entry to a ledger file at `/home/user/config_ledger.txt`.
   - The ledger entry format must be exactly: `[UPDATE] <relative_archive_path> | <key>=<value>` for each key-value pair found in the file. 

**Execution:**
Once your script is written, run it against the archive `/home/user/incoming/updates.zip` with the target directory `/home/user/app_configs`. 

Make sure the required directories are created if they do not exist. After your script finishes, the valid configurations must be extracted, the malicious paths logged, and the ledger file generated.