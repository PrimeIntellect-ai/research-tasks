You are a backup operator tasked with testing an automated restore procedure for a simulated remote branch located in Tokyo. You need to write an idempotent Bash script that handles the restore process and schedule it.

The backup archive is located at `/home/user/backup.tar.gz`. Inside this archive are two files: `data.txt` and `backup.log`. The `backup.log` file contains lines starting with a Unix epoch timestamp followed by a message (e.g., `1688169600 Backup verified`).

Please complete the following tasks:

1. Write a Bash script at `/home/user/restore_test.sh` and make it executable.
2. The script must be **idempotent**. When executed, it should check if `/home/user/restored_data/data.txt` already exists. If it does NOT exist, the script must create the `/home/user/restored_data` directory (if needed) and extract the contents of `/home/user/backup.tar.gz` directly into it. If the file already exists, it should skip the extraction step entirely.
3. The script must read `/home/user/restored_data/backup.log`. For every line in the log, it must convert the Unix epoch timestamp to a human-readable date in the `Asia/Tokyo` timezone, formatted exactly as `YYYY-MM-DD HH:MM:SS`. It should output the transformed lines to `/home/user/restore_report.txt` in the format: `[YYYY-MM-DD HH:MM:SS] The rest of the message`. Overwrite `/home/user/restore_report.txt` if it exists.
4. Schedule this script to run daily at 3:00 AM by adding it to the current user's crontab. Write the exact cron schedule line to `/home/user/cron_backup.txt` and load it into the user's crontab.

Example of log transformation:
If `backup.log` contains: `1688169600 System snapshot taken`
The output in `/home/user/restore_report.txt` must be: `[2023-07-01 09:00:00] System snapshot taken`

Ensure your script works cleanly without requiring root access.