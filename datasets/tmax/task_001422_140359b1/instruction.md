I am a cloud architect migrating a set of legacy services to our new cloud infrastructure. As part of this migration, I need you to implement an automated log processing, backup, and alerting pipeline. Our environment lacks root privileges, so all configurations must occur within my user directory.

Please perform the following steps:

1. **Text Processing Pipeline**
There is a legacy log file located at `/home/user/legacy_logs/app.log`. 
Write a shell script `/home/user/migration/parse_logs.sh` that uses text processing tools (like `awk`, `sed`, or `grep`) to extract all lines containing the string `[CRITICAL]`.
Format the output by replacing the ` [CRITICAL] ` tag with ` | ` (a space, a pipe, and a space). 
Save the resulting formatted lines to `/home/user/migration/critical_summary.txt`.
Make the shell script executable and run it.

2. **Backup and Rotation Script**
Write a Python script at `/home/user/migration/migrator.py` that performs a backup of the legacy data directory located at `/home/user/app_data/`.
The script must:
- Create a `tar.gz` archive of the `/home/user/app_data/` directory.
- Save the archive in `/home/user/backups/` with the naming convention `backup_YYYYMMDD_HHMMSS.tar.gz` (using the current time).
- Implement a backup rotation strategy: immediately after creating the new backup, inspect `/home/user/backups/`. If there are more than 3 backup archives (`.tar.gz` files), delete the oldest ones based on file modification time so that exactly the 3 most recent backups remain.

3. **Email Alerting**
Extend the `migrator.py` script to check the line count of `/home/user/migration/critical_summary.txt`.
If there are strictly more than 5 lines in this file, the script must connect to a local unauthenticated SMTP server running on `localhost` port `8025` and send an email alert.
The email must have:
- Sender: `migrator@cloudops.local`
- Recipient: `admin@cloudops.local`
- Subject: `Migration Alert: Critical Errors Detected`
- Body: The exact contents of the `critical_summary.txt` file.

4. **Execution**
Run your Python script (`python3 /home/user/migration/migrator.py`) to trigger the backup, rotation, and alerting logic.

Ensure all file paths and exact output formats are strictly followed. Note: A mock SMTP server will be listening on port 8025, do not attempt to start one yourself.