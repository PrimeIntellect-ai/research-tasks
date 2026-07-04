You are a cloud architect migrating a custom log-processing service to a new non-root containerized environment. In the old system, a systemd service managed the startup order, ensuring that storage directories and configuration files were created before the process supervisor started. Because we cannot use systemd in this environment, you need to fix the C-based process supervisor, recreate the startup dependency logic, and write an analysis pipeline for the generated logs.

Your task consists of three parts. All work must be done in `/home/user`.

**Part 1: Idempotent Setup and Startup Scripting**
The old service relied on systemd `ExecStartPre` and `After=` directives to ensure storage was set up.
1. Write an idempotent shell script `/home/user/init_storage.sh` that:
   - Creates the directory `/home/user/app_data` if it does not exist.
   - Creates a file `/home/user/app_data/quota_config` containing exactly `QUOTA=8192` if the file does not already exist. If it exists, it must not overwrite it.
   - Ensures the script exits with code 0.
2. Write a script `/home/user/start_services.sh` that:
   - First executes `/home/user/init_storage.sh`.
   - Then runs the compiled `./supervisor` executable in the background.
   - Exits with code 0.

**Part 2: Fixing the C Process Supervisor**
There is a C program located at `/home/user/supervisor.c`. It is designed to read the quota configuration, spawn a mock worker (`/home/user/worker.sh`), and monitor it. 
Currently, it has two critical issues:
1. It suffers from a race condition/crash similar to a missing dependency: if `/home/user/app_data/quota_config` is missing or unreadable, `fopen()` returns `NULL`, and the program immediately segfaults when trying to read from it.
2. It has hardcoded the quota limit instead of parsing it from the configuration file.

Modify `/home/user/supervisor.c` so that:
- It safely handles the case where `fopen()` fails (e.g., print an error and `exit(1)` instead of segfaulting).
- It reads the file `/home/user/app_data/quota_config`, parses the integer value after `QUOTA=` (e.g., `8192`), and stores it in the `max_quota` variable.
- Compile your fixed code: `gcc -o /home/user/supervisor /home/user/supervisor.c`

**Part 3: Text Processing Pipeline**
The worker script writes telemetry data to `/home/user/app_data/metrics.log`. Each line has the format:
`[TIMESTAMP] [LEVEL] [VALUE] [MESSAGE]`
Example: `2023-10-10T10:00:00 CRITICAL 405 Storage degraded`

Write a shell script `/home/user/parse_metrics.sh` that:
- Uses text processing tools (`awk`, `grep`, `sed`, etc.) to process `/home/user/app_data/metrics.log`.
- Finds all lines where the log level is exactly `CRITICAL`.
- Extracts the numeric value (the 3rd column).
- Sums all these numeric values together.
- Writes the final total sum as a single integer to `/home/user/critical_sum.txt`.

Ensure all scripts are marked as executable (`chmod +x`). Once you are done, run `/home/user/start_services.sh`, wait 3 seconds, and then run `/home/user/parse_metrics.sh`.