You are tasked with fixing and configuring a custom health monitoring and backup service for our server. The service is written in C, but it is currently failing to execute backups correctly because it is designed to run in a restricted environment (like a cron job) where standard environment variables like `PATH` are not fully populated, and it relies on a custom `fstab`-like file for its configuration.

Here is the current situation:
1. There is a backup script located at `/home/user/local_bin/perform_backup.sh`. It takes two arguments: the destination directory and a status message.
2. We need to simulate a mount point for backups. Create a directory `/home/user/mnt/backup_drive`.
3. Create a configuration file at `/home/user/custom_fstab` that mimics a standard Linux `/etc/fstab` file. Add a single entry to it:
   `monitor_fs /home/user/mnt/backup_drive customfs defaults 0 0`
4. There is a buggy C program located at `/home/user/monitor.c`. It is supposed to:
   - Perform a health check (always succeeds for this scenario).
   - Read `/home/user/custom_fstab` to find the mount point for the device named `monitor_fs`.
   - Call the backup script with the extracted mount point and the message `SYSTEM_HEALTHY`.

However, the C program has a few issues:
- It currently hardcodes the backup path instead of parsing `/home/user/custom_fstab`.
- It attempts to call `perform_backup.sh` directly using `system()`, which fails because `/home/user/local_bin` is not in the default `PATH`, a common issue when scripts run via cron.

Your task:
1. Create the required directory `/home/user/mnt/backup_drive`.
2. Create the `/home/user/custom_fstab` file with the exact specification above.
3. Modify `/home/user/monitor.c` so that it parses `/home/user/custom_fstab` to extract the correct mount point (the second column) for the line starting with `monitor_fs`.
4. Fix the `system()` call in `/home/user/monitor.c` so that it successfully executes `/home/user/local_bin/perform_backup.sh` with the extracted mount point and the string `SYSTEM_HEALTHY`. You can do this by using the absolute path to the script in the `system()` command.
5. Compile the C program to `/home/user/monitor_daemon`.
6. Run `/home/user/monitor_daemon`.

If successful, the `perform_backup.sh` script will create a file named `health_status.log` inside `/home/user/mnt/backup_drive` containing the message. Ensure the program is executed and the file is created successfully.