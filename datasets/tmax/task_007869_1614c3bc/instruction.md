You are acting as a capacity planner analyzing resource usage on a Linux system. You need to deploy a lightweight, custom resource monitor written in C that logs memory and load averages. Since this deployment will be rolled out to many user-space environments, you must write an idempotent deployment script to set up the directory structure, compile the code, and manage symlinks without requiring root privileges.

Perform the following tasks:

1. **Write the C Monitor (`/home/user/monitor_src/resource_monitor.c`)**
   Write a C program that does the following:
   - Takes exactly one command-line argument: the absolute path to the output log file.
   - Reads the 1-minute load average from `/proc/loadavg`.
   - Reads `MemTotal` and `MemFree` from `/proc/meminfo`.
   - Calculates `MemUsed` as `MemTotal - MemFree`.
   - Appends a single line to the specified log file in the following CSV format: `<unix_timestamp>,<load_1_min>,<mem_used_kb>,<mem_total_kb>`
   - Exits with code 0 on success, or non-zero on failure.

2. **Write an Idempotent Deployment Script (`/home/user/deploy.sh`)**
   Write a bash script that performs the following setup. It must be completely idempotent (running it multiple times must not fail, duplicate data, or create nested symlinks).
   - Creates the directory `/home/user/monitor_src` (if it doesn't exist, though you will place your C code there).
   - Creates the deployment directories: `/home/user/deploy/bin` and `/home/user/deploy/logs`.
   - Sets the permissions of `/home/user/deploy/bin` to `700`.
   - Compiles `/home/user/monitor_src/resource_monitor.c` using `gcc` into the executable `/home/user/deploy/bin/monitor`.
   - Creates an empty log file at `/home/user/deploy/logs/active.csv` if it does not already exist.
   - Creates or updates a symbolic link at `/home/user/deploy/current_log` that points to `/home/user/deploy/logs/active.csv`.

3. **Execution**
   - Create the source directory and write your C code.
   - Write your deployment script.
   - Make your deployment script executable and run it.
   - Execute the compiled monitor program exactly once, passing the symlink `/home/user/deploy/current_log` as the argument:
     `/home/user/deploy/bin/monitor /home/user/deploy/current_log`