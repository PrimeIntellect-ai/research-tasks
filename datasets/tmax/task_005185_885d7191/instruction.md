You are an edge computing engineer configuring an IoT gateway device. The device collects high-frequency sensor data, but has very limited storage capacity and operates on intermittent networks. You need to implement a localized log rotation and storage monitoring system to ensure the device doesn't run out of disk space, and alerts the central server (via a local mail spool relay) when capacity thresholds are breached.

Your task is to configure the log rotation, write a storage monitoring script, and create a master wrapper script. 

Follow these requirements precisely:

1. **Log Rotation Configuration**:
   Create a logrotate configuration file at `/home/user/iot_logrotate.conf`. 
   It must manage all files matching `/home/user/edge_storage/logs/*.log`.
   The configuration must enforce the following rules:
   - Rotate the log file if it exceeds `5M` (5 Megabytes).
   - Keep exactly `2` rotated backups.
   - Compress the rotated logs.
   - Do not throw an error if the log file is missing (`missingok`).
   - Do not mail the log files (`nomail`).

2. **Storage Monitoring Script**:
   Create a bash script at `/home/user/check_storage.sh` and make it executable.
   The script must:
   - Calculate the total disk usage of the `/home/user/edge_storage` directory in Megabytes (MB). Round up or down to the nearest integer.
   - If the total size is strictly greater than `20` MB, it must send an alert email using the mock mail relay agent provided at `/home/user/bin/mock_sendmail`.
   - The email must have the exact header: `Subject: ALERT: IoT Storage High`
   - The email body must contain the exact string: `Current usage: X MB` (where X is the calculated integer size in MB).
   - Pass the email to the mock sendmail command via standard input (e.g., `echo -e "Subject: ...\n\nCurrent usage: ..." | /home/user/bin/mock_sendmail`).

3. **Master Daemon Script**:
   Create an executable bash script at `/home/user/edge_daemon.sh`.
   This script must perform the following actions in order:
   - Execute `logrotate` using your config file (`/home/user/iot_logrotate.conf`). Since you do not have root access, you must explicitly specify a state file located at `/home/user/logrotate.status`.
   - Execute your storage monitoring script (`/home/user/check_storage.sh`).

Make sure all scripts have the appropriate executable permissions (`chmod +x`). Do not run the daemon script yourself; the automated test suite will generate test log files and run `/home/user/edge_daemon.sh` to verify your solution.