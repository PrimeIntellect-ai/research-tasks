You are tasked with building a secure configuration change tracker. We receive system configuration backups as tar archives, but we've recently experienced an incident where a malicious backup archive attempted to overwrite system files using a "zip slip" (path traversal) attack. 

You must write a Python script at `/home/user/config_tracker.py` that processes a backup archive in a secure, memory-efficient manner without extracting it to disk.

**Input Files:**
1. `/home/user/tracker_config.ini`: A configuration file specifying the tracking rules.
2. `/home/user/backup.tar`: An uncompressed tar archive containing the configuration files.

**Requirements for `/home/user/config_tracker.py`:**
1. **Configuration Parsing:** Read `/home/user/tracker_config.ini`. It contains a `[Settings]` section with `target_dir` (the base directory where files *would* be extracted) and `allowed_exts` (a comma-separated list of allowed file extensions).
2. **Streaming I/O:** Open `/home/user/backup.tar` in streaming mode. Do not extract the archive to disk or load the entire archive into memory at once. Process it entry by entry.
3. **Security Validation (Zip-Slip Prevention):** For each entry in the tar archive, determine its intended absolute path if it were to be extracted into the `target_dir`. If the intended extraction path does not strictly begin with the `target_dir` (e.g., due to absolute paths like `/etc/shadow` or relative path traversals like `../../malicious`), you must:
   - Reject the file.
   - Append a warning line to `/home/user/security_alerts.log` exactly in this format: `ALERT: Path traversal detected - <original_tar_name>`
4. **Manifest and Checksum Generation:** For all secure files that also end with one of the `allowed_exts`, read their contents from the tar stream and compute their SHA256 checksum. 
5. **Output:** Generate a JSON manifest at `/home/user/manifest.json`. The JSON should be a flat dictionary mapping the secure, intended absolute path of the file (e.g., `/home/user/extracted/nginx/nginx.conf`) to its SHA256 checksum hex string.

**Execution:**
Once your script is written, execute it. Ensure `/home/user/manifest.json` and `/home/user/security_alerts.log` are successfully created according to the specifications.