You are a backup administrator auditing a set of incoming backup archives. We suspect one of the automated backup sources has been compromised and is attempting a "Zip Slip" path traversal attack by including malicious paths (e.g., paths starting with `../` or `/`) inside the archive.

You need to analyze the archives located in `/home/user/backups/` without extracting them, isolate the malicious archive, and securely manifest the safe ones.

Perform the following tasks using Bash and command-line tools:
1. Examine all `.zip` archives in `/home/user/backups/`.
2. Identify the malicious archive containing at least one path traversal payload (a file path attempting to escape the extraction directory using `../`).
3. Write the exact basename of the malicious archive (e.g., `backup_99.zip`) to `/home/user/malicious_archive.txt`.
4. Extract the manifest (list of file paths) contained inside the malicious archive and write it to `/home/user/malicious_payload_files.txt`. Each line should contain just the file path as stored in the archive.
5. For all the remaining *safe* `.zip` files, verify their archive integrity. Assuming they are intact, generate a SHA256 checksum manifest. Write the standard `sha256sum` output for these safe files to `/home/user/safe_backups.sha256`. The paths in the manifest must be the basenames of the files (e.g., run the checksum from within the backups directory).

Do not actually extract the archives to disk, as this could trigger the payload.