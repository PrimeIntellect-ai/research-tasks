You are a storage administrator managing disk space and processing incoming backup archives. Your system uses a custom text-based archive format for small configuration backups, but a recent security audit revealed that malicious actors might inject absolute paths or path traversal strings (`../`) into these archives to overwrite critical files (a vulnerability known as "Zip Slip").

Your task is to write a robust Bash script at `/home/user/process_backup.sh` that safely parses and extracts these custom archives, completely mitigating path traversal attacks.

The incoming archive is located at `/home/user/incoming/backup.dat`. 

The archive format consists of repeating blocks for each file:
```
PATH: <filepath>
B64DATA: <base64_encoded_content>
```
There are no empty lines between blocks. 

Your script must perform the following actions:
1. Parse `/home/user/incoming/backup.dat`.
2. Evaluate the `<filepath>` of each entry. 
   - If the path starts with a `/` (absolute path) OR contains the substring `../` anywhere, it is considered malicious.
   - For malicious paths, DO NOT extract the file. Instead, append the exact malicious path string to `/home/user/quarantine.log` on a new line.
3. For safe paths, decode the Base64 content and write it to the target directory: `/home/user/safe_restore/`. 
   - You must recreate any necessary directory structure inside `/home/user/safe_restore/` (e.g., if the safe path is `configs/app.conf`, it should be written to `/home/user/safe_restore/configs/app.conf`).
4. After processing the entire archive, generate a SHA-256 checksum manifest of all safely extracted files. 
   - Use the `sha256sum` command. 
   - Save the output to `/home/user/restore_checksums.txt`. Run the checksums from inside the `/home/user/safe_restore/` directory so the paths in the manifest are relative (e.g., `configs/app.conf` instead of `/home/user/safe_restore/configs/app.conf`).
   - The manifest must be sorted alphabetically by file path.
5. Finally, use an atomic write pattern (write to a temporary file, then use `mv`) to create a status file at `/home/user/restore_status.txt` containing the exact text `EXTRACTION COMPLETE`.

Ensure your script is executable and run it to process the archive.