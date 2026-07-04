You are acting as a backup operator responding to a critical incident. You need to identify a specific backup, verify its integrity against malicious tampering, and restore a virtualized service from it to extract a system state report.

Here are your instructions:

1. **Identify the Target Backup:**
   An automated voicemail from the incident response team has been saved to `/app/incident_report.wav`. Transcribe this audio file to find the "Target Restore ID". It will be a short alphanumeric code spoken in the recording.

2. **Develop a Backup Sanitizer:**
   Recent backups may have been tampered with by a threat actor injecting malicious files into the tar archives. 
   Write a Python script at `/home/user/verify_backup.py` that takes exactly one argument (the path to a `.tar` or `.tar.gz` file). 
   The script must inspect the contents of the archive *without extracting it* and determine if it is safe.
   It must exit with status code `0` if the archive is safe, and exit with status code `1` if the archive is "evil".
   An archive is considered "evil" if ANY of the following are true for any member in the archive:
   - The file path is absolute (starts with `/`).
   - The file path contains directory traversal sequences (`../`).
   - The file has the setuid or setgid permission bits set.
   
   Your script will be tested against an automated test suite containing known clean and evil archives.

3. **Restore and Run the VM:**
   Check the directory `/app/staging_backups/`. There are several backup archives here.
   Find the archive that contains your "Target Restore ID" in its filename AND is marked as safe by your `verify_backup.py` script.
   Extract this safe archive into `/home/user/restore/`.
   Inside, you will find a raw QEMU disk image (`disk.img`) and a startup script (`start_vm.sh`).
   Execute the startup script in the background to boot the VM using user-mode QEMU. 
   
4. **Extract the Report:**
   The VM will initialize a systemd service that exposes a local HTTP endpoint on port `8080`.
   Wait for the service to become available, then make a GET request to `http://127.0.0.1:8080/report`.
   Save the exact response body to `/home/user/restore_report.txt`.

Ensure your `verify_backup.py` script is robust, as the automated verification will strictly test it against a hidden corpus of archives.