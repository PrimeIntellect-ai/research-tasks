You are a backup operator automating a restore testing pipeline. Because you are testing locally without root privileges, you are working with simulated environments and user-space tools.

Your task is to write a single, robust Python script at `/home/user/restore_automation.py` that performs the following steps end-to-end:

1. **Interactive Authentication (Expect):**
   There is an interactive binary located at `/home/user/tools/fetch_backup`. It simulates a secure backup retrieval. When executed, it prompts exactly with: `Operator PIN: `. 
   Use Python's `pexpect` module to automate this interaction. The PIN you must send is `8374`. Upon success, the tool will generate a backup archive at `/home/user/backup.tar`.

2. **Extraction / Simulated Mount:**
   Ensure the directory `/home/user/mnt_restore` exists. Extract the contents of `/home/user/backup.tar` into this directory.

3. **Fstab Configuration:**
   You have a simulated root filesystem. Modify the fstab file located at `/home/user/mock_root/etc/fstab`. Append a new line to this file to represent the mounting of the backup. The line must exactly match:
   `/home/user/backup.tar /home/user/mnt_restore tarfs ro,nosuid,nodev 0 0`
   Make sure to preserve all existing entries in the file.

4. **User Verification:**
   The extracted backup contains a file `/home/user/mnt_restore/metadata.json` which specifies a username. Parse this JSON file. Next, check the simulated passwd file at `/home/user/mock_root/etc/passwd`. If the username found in the JSON exists in the simulated passwd file, write the string `USER_VERIFIED: <username>` to a log file at `/home/user/restore_status.log`. If it does not exist, write `USER_NOT_FOUND`.

5. **Port Forwarding & Firewall (Network):**
   The restored backup contains a service that runs on port 8080 (already mocked by a background process). Implement a simple TCP proxy server within your Python script that listens on `127.0.0.1:9999` and forwards traffic to `127.0.0.1:8080`. 
   *Firewall Rule:* Your proxy must inspect the client's IP. Only forward traffic if the source IP is exactly `127.0.0.1`. If it is any other IP, gracefully close the connection without forwarding.
   Run this proxy in a background thread or process within your script so the script does not block forever, and leave it running for at least 5 seconds before the script exits (or just leave it running and let the test suite kill it).

Make sure your Python script handles errors gracefully. You can run `python3 /home/user/restore_automation.py` to test your work.