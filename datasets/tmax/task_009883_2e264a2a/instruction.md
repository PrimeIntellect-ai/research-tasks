You are an observability engineer tuning custom dashboards. We need a lightweight, custom metric exporter written in C to monitor the status of specific simulated mount points, along with an idempotent bash script to manage the deployment and lifecycle of this exporter daemon.

Your task has two main parts:

**Part 1: The Exporter (C Program)**
Write a C program at `/home/user/exporter.c` that acts as a continuous metric exporter. 
1. The program should read a custom fstab-formatted configuration file located at `/home/user/dashboard_fstab.conf`.
2. Parse the file to extract the mount point paths (which is the 2nd column in standard fstab syntax: `<device> <mount_path> <type> <options> <dump> <pass>`). Ignore empty lines or lines starting with `#`.
3. Enter an infinite loop where, every 1 second, it checks if each extracted directory path exists (e.g., using `access()`).
4. During each iteration, write the status of all paths to a temporary file `/home/user/dashboard/metrics.tmp`. The format for each line must be exactly:
   `mount_active{path="<mount_path>"} <status>`
   where `<status>` is `1` if the directory exists, and `0` if it does not.
5. After writing all paths in the iteration, atomically rename the temporary file to `/home/user/dashboard/metrics.prom`.

**Part 2: The Deployment Script (Bash)**
Write an idempotent bash script at `/home/user/deploy.sh` that manages the lifecycle of this exporter:
1. Ensure the directory `/home/user/dashboard` exists.
2. Compile `/home/user/exporter.c` to an executable named `/home/user/exporter` using `gcc`.
3. Check if the exporter is already running by looking for a PID in `/home/user/exporter.pid`. If a process with that PID is running, safely terminate it (kill).
4. Start the newly compiled `/home/user/exporter` in the background (as a daemon).
5. Save the new background process's PID into `/home/user/exporter.pid`.

Make sure `/home/user/deploy.sh` has executable permissions.
The task is complete when you have successfully run `/home/user/deploy.sh` and the metrics are being actively exported to `/home/user/dashboard/metrics.prom`.