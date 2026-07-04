You are a systems engineer hardening the monitoring and backup procedures for a set of lightweight virtual machines. As part of this, you need to develop a custom user-space daemon in C to monitor QEMU raw disk images, trigger backups automatically when they grow beyond a certain size, and manage the resulting logs.

Since you do not have root access, you will deploy all components within your home directory (`/home/user`).

Please complete the following phases:

**Phase 1: Environment Setup**
1. Create the necessary directories: `/home/user/logs` and `/home/user/backups`.
2. Use `qemu-img` to create a raw virtual disk image named `/home/user/vm_disk.img` with an initial size of 10 Megabytes.

**Phase 2: C Monitor Daemon**
1. Write a C program at `/home/user/disk_monitor.c`.
2. The program must compile successfully to an executable named `/home/user/disk_monitor` (using `gcc`).
3. The C program must:
   - Accept exactly three command-line arguments: `<path_to_watch>` `<threshold_in_bytes>` `<script_to_run>`.
   - Run in an infinite loop, polling the file size of `<path_to_watch>` every 1 second (using `stat`).
   - If the file size is strictly greater than `<threshold_in_bytes>`, it must:
     a. Append a log entry to `/home/user/logs/monitor.log` in the exact format: `THRESHOLD_EXCEEDED: <size_in_bytes>\n`
     b. Execute the script specified in `<script_to_run>` using the `system()` call.
     c. Exit immediately after triggering the script and logging the event once (for the purpose of this task, it doesn't need to stay running after the first trigger).

**Phase 3: Backup Script**
1. Write a bash script at `/home/user/backup.sh` and make it executable.
2. When executed, this script must copy `/home/user/vm_disk.img` to the `/home/user/backups/` directory.
3. The copied file must be named `vm_disk_backup_<TIMESTAMP>.img`, where `<TIMESTAMP>` is the current UNIX epoch time (e.g., `vm_disk_backup_1690000000.img`).
4. The script must then ensure that ONLY the 3 most recent backup files remain in `/home/user/backups/`. If there are more than 3, delete the oldest ones.

**Phase 4: User-level Log Rotation**
1. Write a `logrotate` configuration file at `/home/user/logrotate.conf`.
2. Configure it to rotate `/home/user/logs/monitor.log`. It should keep exactly 2 old backups, compress them (`.gz`), and rotate them based on size (rotate if larger than 10 bytes). 

**Phase 5: Execution and Verification**
1. Run your compiled `disk_monitor` in the background (or another terminal) watching `/home/user/vm_disk.img` with a threshold of `15000000` (15MB), and pointing to `/home/user/backup.sh`.
2. While the monitor is running, simulate the VM disk growing by resizing `/home/user/vm_disk.img` to 20 Megabytes (using `qemu-img resize`).
3. Wait for the monitor to detect the change, log the event, and trigger the backup.
4. Run `logrotate -f /home/user/logrotate.conf` manually in the terminal to force the log rotation and prove your log rotation configuration works.

When you are done, leave the generated files, the compiled binary, the rotated logs, and the backup in place.