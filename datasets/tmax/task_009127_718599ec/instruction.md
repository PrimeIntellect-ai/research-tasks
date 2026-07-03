You are a backup operator tasked with automating the testing of restores from a legacy interactive backup system. 

We have a legacy restore script located at `/home/user/legacy_restore.sh` that we need to test automatically. The script is strictly interactive and cannot take command-line arguments. 

Your task consists of three parts:

1. **Interactive Automation (`expect`)**:
   Write an `expect` script at `/home/user/run_restore.exp` that executes `/home/user/legacy_restore.sh` and automates the responses to its prompts. 
   The script will prompt for the following exactly in this order:
   - "Enter decryption passphrase: " -> You must answer `secure_backup_2024`
   - "Target restore path: " -> You must answer `/home/user/recovered_data`
   - "Proceed with restore? (yes/no): " -> You must answer `yes`
   
   Execute your `expect` script so that the restore runs. Upon success, the legacy script will create the target directory and write a log file to `/home/user/restore_activity.log`.

2. **Text Processing (`awk`/`grep`)**:
   The generated `/home/user/restore_activity.log` contains various log levels. Extract all lines that contain the exact word `[RESTORED]`. Using text processing tools, extract only the file paths (which will be the 4th space-separated field in the log line) and save them, one per line, to `/home/user/restored_files.txt`.

3. **Log Configuration**:
   Create a local logrotate configuration file at `/home/user/test_logrotate.conf` to manage `/home/user/restore_activity.log`. 
   The configuration for this file must include the following directives:
   - Rotate daily (`daily`)
   - Keep 5 rotations (`rotate 5`)
   - Compress old logs (`compress`)
   - Ignore missing log files (`missingok`)
   - Create a new empty log file after rotation with 0644 permissions for user `user` and group `user` (`create 0644 user user`)

Ensure all scripts are run and the final output files (`/home/user/restored_files.txt` and `/home/user/test_logrotate.conf`) are correctly placed.