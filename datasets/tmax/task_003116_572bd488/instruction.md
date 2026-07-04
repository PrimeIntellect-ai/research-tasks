You are tasked with building a lightweight Kubernetes "operator" simulator in C, along with its deployment pipeline and log management configuration. Since you do not have root access, everything will be configured in user-space inside the `/home/user` directory.

Complete the following objectives:

1. **C Operator Implementation**:
   Write a C program at `/home/user/src/operator.c`. This program must:
   - Read the directory `/home/user/manifests`.
   - Iterate through all files ending in `.yaml`.
   - For each matching file, append the exact line `[SUCCESS] Deployed <filename>` (where `<filename>` is the name of the file, not the full path) to the log file `/home/user/logs/operator.log`.
   - Ensure the program compiles successfully with `gcc /home/user/src/operator.c -o /home/user/bin/operator`. (You must compile it).

2. **Log Rotation Configuration**:
   Create a local logrotate configuration file at `/home/user/logrotate.conf` specifically for `/home/user/logs/operator.log`. It must specify:
   - Daily rotation.
   - Keep exactly 3 rotated backups.
   - Compress the rotated logs.
   - Create a new log file after rotation.

3. **Scheduled Task Configuration (Cron)**:
   Create a crontab file at `/home/user/operator.cron` that schedules the execution of `/home/user/bin/operator` to run every 5 minutes. 
   Apply this configuration to the user's crontab using the `crontab` command.

4. **CI/CD Pipeline Script**:
   Create a bash script at `/home/user/build_and_test.sh` that simulates a CI pipeline. The script must:
   - Be executable.
   - Compile the C program from `/home/user/src/operator.c` to `/home/user/bin/operator`.
   - Create a dummy manifest file named `/home/user/manifests/ci-test.yaml`.
   - Run the compiled operator binary.
   - Check if `/home/user/logs/operator.log` contains the string `[SUCCESS] Deployed ci-test.yaml`.
   - If it does, print exactly `CI PASSED` to standard output and exit with status `0`.
   - If it does not, print `CI FAILED` to standard output and exit with status `1`.

Note: You may need to create the directories `/home/user/src`, `/home/user/bin`, `/home/user/manifests`, and `/home/user/logs` if they do not exist.