You are tasked with writing a secure configuration update manager in Python. 

A system periodically receives nested archives containing configuration updates in JSON format. We have received a new update archive at `/home/user/incoming/update.zip`. This zip file contains a tarball named `payload.tar`.

Your objective is to write and execute a Python script at `/home/user/process_update.py` that does the following:
1. Extracts `payload.tar` from `/home/user/incoming/update.zip`.
2. Safely extracts the contents of `payload.tar` into the directory `/home/user/configs/`.
   * **Security Requirement:** You must protect against "zip slip" or path traversal attacks. The tarball may contain files with malicious paths (e.g., `../../evil.sh`) or symlinks that point outside the target directory. Your script must absolutely prevent any file from being written, overwritten, or linked outside of `/home/user/configs/`. Skip any files or links in the tarball that attempt to escape the target directory.
3. Overwrite any existing JSON configurations in `/home/user/configs/` if a valid, safe file with the same name is extracted.
4. After extraction, parse all `.json` files currently in `/home/user/configs/`. Every valid config file contains a `"version"` key at the root level (e.g., `{"version": "1.2"}`).
5. Generate a CSV report at `/home/user/config_summary.csv` with the headers `filename,version`. List all JSON files found in `/home/user/configs/` sorted alphabetically by filename.

Ensure your script handles everything programmatically and securely. Once you have written the script, execute it to update the configurations and generate the CSV.