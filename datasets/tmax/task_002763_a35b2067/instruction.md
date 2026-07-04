You are a FinOps analyst tasked with optimizing cloud storage costs and managing application logs on a Linux server to prevent disk space exhaustion. You need to implement a deduplication strategy for tenant configuration files and a custom log monitoring and rotation system using C and Bash.

The system has the following existing structures:
1. A billing service continuously writes to a log file at `/home/user/logs/billing.log`. The PID of this service is stored in `/home/user/logs/billing.pid`. When this process receives a `SIGUSR1` signal, it gracefully reopens its log file.
2. Several tenant directories exist under `/home/user/tenants/`. Each contains a `config.json` file. Many of these configuration files are completely identical to the baseline configuration located at `/home/user/tenants/baseline/config.json`, wasting EBS volume space.

Perform the following tasks:

**Task 1: Tenant Deduplication (Link and Directory Management)**
Write a bash script at `/home/user/link_assets.sh`. When executed, this script must scan all directories matching `/home/user/tenants/tenant_*`. For any `config.json` file that has the exact same content as `/home/user/tenants/baseline/config.json`, replace it with a hard link to the baseline file. Files that differ from the baseline must be left untouched. Execute this script to perform the deduplication.

**Task 2: Log Rotation Script**
Create a bash script at `/home/user/rotate.sh` and make it executable. When run, it must:
1. Rotate `/home/user/logs/billing.log` keeping up to 3 old logs (`billing.log.1`, `billing.log.2`, `billing.log.3`). (e.g., `billing.log.2` becomes `billing.log.3`, `billing.log.1` becomes `billing.log.2`, and the current `billing.log` becomes `billing.log.1`).
2. Send a `SIGUSR1` signal to the process whose PID is inside `/home/user/logs/billing.pid` so it starts writing to a fresh `billing.log`.

**Task 3: Custom Log Monitor (Process Monitoring in C)**
Write a C program at `/home/user/monitor.c` and compile it to `/home/user/monitor`.
This program must take exactly two command-line arguments:
`./monitor <file_path> <max_size_bytes>`

The program should run in an infinite loop doing the following:
1. Check the file size of `<file_path>`.
2. If the size strictly exceeds `<max_size_bytes>`, invoke your script `/home/user/rotate.sh` (using `system()` or `exec`).
3. Sleep for 1 second before checking again.

Ensure your code handles basic errors (e.g., file not found). You do not need to leave the C program running in the background for the final evaluation, but the source code, the compiled binary, and the bash scripts must be correct and present in `/home/user`.