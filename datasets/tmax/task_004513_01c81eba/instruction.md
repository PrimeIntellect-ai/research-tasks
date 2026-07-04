You are an artifact manager responsible for curating a repository of binary distributions. Recently, there have been supply chain attacks using "Zip Slip" vulnerabilities, where malicious actors upload archives containing files with absolute paths (e.g., `/etc/passwd`) or directory traversal paths (e.g., `../../root/.ssh/authorized_keys`). If extracted naively, these overwrite critical system files outside the target directory. 

Additionally, some uploaded archives get corrupted during transit.

Your task is to write and execute a Bash script at `/home/user/audit.sh` that processes a backlog of archives located in `/home/user/incoming_artifacts`.

For every `.tar.gz` and `.zip` file in `/home/user/incoming_artifacts`, your script must perform the following actions:

1. **Vulnerability Scan**: Inspect the file paths inside the archive *without* extracting it. Use text transformation tools (`awk`, `sed`, or similar) to parse the archive's file list. An archive is considered "MALICIOUS" if it contains any path that starts with `/` or contains the substring `../`.
2. **Integrity Check**: If the archive is not malicious, verify its structural integrity (e.g., using `unzip -t` or `tar -tzf`). If it fails the integrity check, it is considered "CORRUPT".
3. **Routing & Extraction**:
   - If **MALICIOUS**: Move the archive to `/home/user/quarantine/`.
   - If **CORRUPT**: Move the archive to `/home/user/quarantine/`.
   - If **SAFE** (neither malicious nor corrupt): Extract the archive's contents into a new subdirectory inside `/home/user/safe_artifacts/`. The subdirectory must be named exactly after the archive file *without* its extension (e.g., `app_v1.tar.gz` extracts into `/home/user/safe_artifacts/app_v1/`). Then, move the original archive to `/home/user/processed/`.
4. **Logging**: For each processed file, append exactly one line to `/home/user/artifact_audit.log` using the following strict format:
   `<filename> | <STATUS> | <detail>`
   
   - `<filename>` is just the name of the archive (e.g., `payload.zip`).
   - `<STATUS>` is `MALICIOUS`, `CORRUPT`, or `SAFE`.
   - `<detail>`:
     - For `MALICIOUS`: The exact string of the *first* malicious file path found in the archive's listing.
     - For `CORRUPT` and `SAFE`: The exact string `N/A`.

Run your script to process all existing files in the `/home/user/incoming_artifacts` directory. Ensure `/home/user/artifact_audit.log` is fully populated.