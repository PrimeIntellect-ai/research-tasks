You are acting as a configuration manager tracking changes in a Linux environment.

Your task is to write a Python script at `/home/user/config_tracker.py` that processes a nested backup archive, computes checksums, and identifies which live configuration files have drifted from their backed-up states.

**Directory Structure & Files:**
- **Live Configs:** `/home/user/configs/` (contains the current `*.conf` files)
- **Backup Archive:** `/home/user/backups/backup_v1.tar.gz`

**Requirements for the Python script:**
1. **Nested Archive Handling:** Read `/home/user/backups/backup_v1.tar.gz`. This archive may contain regular `*.conf` files as well as nested archives (`*.zip` or `*.tar.gz`). You must inspect the contents of the main archive and any nested archives to find all files ending in `.conf`. 
2. **Checksum Generation:** For every `.conf` file found within the backup (whether at the root of the backup or inside a nested archive), compute the SHA-256 checksum of its file content.
3. **Manifest Creation:** Output a JSON manifest file at `/home/user/manifest.json`. The keys should be the base filename of the configuration file (e.g., `"app.conf"`) and the values should be the SHA-256 checksum of its content from the *backup*. (Assume all `.conf` base filenames are unique).
4. **Differential Check:** Iterate through all the `.conf` files currently in `/home/user/configs/`. Compare their current SHA-256 checksums to the backup checksums. 
5. **Change Log:** Create a text file at `/home/user/modified.log` containing the base filenames of any files in `/home/user/configs/` that are either **modified** (checksum differs from the backup) or **new** (not present in the backup). Write one filename per line, sorted alphabetically.

The agent should execute the Python script to generate `/home/user/manifest.json` and `/home/user/modified.log`. You may use standard Python libraries (`tarfile`, `zipfile`, `hashlib`, `json`, `os`, etc.). Do not extract the archives to disk; perform the nested archive reading in memory.