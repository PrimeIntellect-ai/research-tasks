You are an edge computing engineer deploying a telemetry aggregation system to an IoT device. The device needs to process local filesystem data, secure the output, and track changes via a strictly validated local Git repository.

You need to perform the following setup in `/home/user`:

1. **C Program (Filesystem Aggregator)**:
   Write a C program at `/home/user/sensor_processor.c` and compile it to `/home/user/sensor_processor`.
   This program must read the directory `/home/user/telemetry_data` (which already exists and contains files).
   For every regular file in that directory, it must print exactly one line to standard output in this format:
   `File: <filename> | Size: <size_in_bytes> | Permissions: <octal_permissions>`
   *(Example: `File: temp_sensor.dat | Size: 1024 | Permissions: 644`)*
   The output must be sorted alphabetically by filename. Ignore directories (including `.` and `..`).

2. **Git Tracking & Hooks**:
   Initialize a new Git repository at `/home/user/iot_sync_repo`.
   Configure a Git `pre-commit` hook (`/home/user/iot_sync_repo/.git/hooks/pre-commit`) using bash, `awk`, and `grep`. 
   The hook must inspect the commit message. It must REJECT the commit (exit with a non-zero status) UNLESS the commit message contains exactly this string on any line:
   `[IoT-Sync] Locale: en_US.UTF-8, Timezone: UTC`

3. **Automation Script**:
   Create a bash script at `/home/user/sync_telemetry.sh`. The script must:
   - Explicitly export the environment variables `TZ=UTC` and `LC_ALL=en_US.UTF-8`.
   - Run the `/home/user/sensor_processor` program and redirect its output to `/home/user/iot_sync_repo/telemetry_report.txt`.
   - Change the permissions of `/home/user/iot_sync_repo/telemetry_report.txt` to strictly read-only for the owner, and no permissions for group/others (`0400`).
   - Navigate to `/home/user/iot_sync_repo`, stage `telemetry_report.txt`, and commit it with the message:
     `[IoT-Sync] Locale: en_US.UTF-8, Timezone: UTC`
     `(New line) Automated telemetry update.`

4. **Scheduled Task**:
   Configure the user's crontab to execute `/home/user/sync_telemetry.sh` exactly every 5 minutes.

Make sure the scripts and hooks are executable. You do not have root access, so ensure all configurations are done within the `user` space. Test your script to ensure the Git commit succeeds and the files have the correct permissions.