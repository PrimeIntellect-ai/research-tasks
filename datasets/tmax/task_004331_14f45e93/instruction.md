You are a Linux systems engineer tasked with hardening a workspace and implementing a custom process monitoring utility. You need to write a C++ monitor, create a scheduling configuration, and draft an fstab configuration for sandboxed mounts.

Please complete the following tasks:

1. **Custom Process Monitor (C++)**:
   Write a C++ program at `/home/user/monitor.cpp` and compile it to an executable named `/home/user/monitor`. 
   The program must accept exactly one argument: a process name (e.g., `./monitor my_daemon`).
   When executed, it should:
   - Scan the system (e.g., via `/proc`) to find the lowest PID matching the given process name.
   - If found, append the exact line: `STATUS: <process_name> IS RUNNING (PID: <pid>)` to `/home/user/logs/process_status.log`.
   - If not found, append the exact line: `STATUS: <process_name> IS NOT RUNNING` to `/home/user/logs/process_status.log`.
   - **Log Rotation:** After writing the new line, count the total number of lines in `/home/user/logs/process_status.log`. If the file has strictly more than 5 lines, rename it to `/home/user/logs/process_status.log.1` (overwriting any existing backup file).
   - **Hardening:** Ensure that the active log file `/home/user/logs/process_status.log` (if it exists) has exactly `600` (`rw-------`) permissions applied to it programmatically by the C++ code.

2. **Scheduling Configuration**:
   We need to run this monitor periodically. Since you don't have root access to install it in the system cron, simply write the standard crontab line required to run `/home/user/monitor qemu-system-x86_64` exactly every 5 minutes.
   Save this single crontab line to `/home/user/monitor_cron`.

3. **Mount Hardening Configuration**:
   To isolate the data processed by our tools, we will use bind mounts. Write an `fstab`-compatible configuration file at `/home/user/sandbox_fstab` containing a single line that binds `/home/user/data` to `/sandbox/data`.
   The filesystem type must be `none`, and the mount options must include exactly `bind,ro,nosuid,nodev`. Dump and pass should be `0 0`.

Make sure to compile your C++ program and verify it works against a dummy process before finishing. Do not run the cron job yourself; just create the configuration files as requested.