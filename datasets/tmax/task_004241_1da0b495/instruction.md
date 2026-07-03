You are a system administrator tasked with automating a legacy interactive backup tool and monitoring its success.

A legacy shell script located at `/home/user/interactive_tool.sh` requires interactive terminal input to create backups. You need to fully automate this process using an Expect script, orchestrate it via a C program acting as a health monitor, and document a filesystem mount configuration.

Please complete the following steps:

1. **Expect Script for Automation**:
   Write an Expect script at `/home/user/automate.exp`. This script must run `/home/user/interactive_tool.sh` and automatically answer its prompts. 
   - When asked for the source directory, it must provide: `/home/user/source_data`
   - When asked for the destination archive, it must provide: `/home/user/backup.tar.gz`
   - When asked to confirm, it must provide: `y`
   Make sure the expect script waits for the backup to complete and exits cleanly.

2. **C Program for Orchestration and Monitoring**:
   Write a C program at `/home/user/backup_manager.c`. This program must:
   - Use `system()` or `fork()/exec()` to execute your Expect script (`/usr/bin/expect /home/user/automate.exp`).
   - Check if the file `/home/user/backup.tar.gz` was successfully created.
   - If the file exists, append the exact string `BACKUP_SUCCESS\n` to `/home/user/monitor.log`.
   - If the file does not exist, append `BACKUP_FAILED\n` to `/home/user/monitor.log`.
   
   Compile your C program to the executable `/home/user/backup_manager`. Run the executable once so that it creates the backup and writes to the monitor log.

3. **Filesystem Configuration (fstab)**:
   We are planning to mount a dedicated backup drive to `/home/user/backup_drive`. Write a single valid `fstab` line into the file `/home/user/fstab.out` that mounts an `ext4` filesystem with UUID `12345678-1234-1234-1234-123456789abc` to `/home/user/backup_drive` with the options `defaults,noatime`, dump flag `0`, and fsck pass `2`.

Ensure all files are created exactly at the specified absolute paths.