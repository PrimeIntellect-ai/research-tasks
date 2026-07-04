You are a Site Reliability Engineer tasked with building a lightweight, custom C-based uptime and filesystem monitor for a legacy application.

Your objective is to write a C program, configure it, set up a mock environment, and run it to produce a specific status log.

Phase 1: Write the Monitor
Create a C program at `/home/user/sre_monitor.c`. The program must do the following:
1. Accept exactly one command-line argument: the path to a configuration file.
2. Read the configuration file, which will contain key-value pairs (one per line) in the format `KEY=VALUE`. It must parse the following keys:
   - `HEARTBEAT_FILE`: The absolute path to a heartbeat file.
   - `DATA_DIR`: The absolute path to a directory whose disk space needs monitoring.
   - `MIN_SPACE_MB`: An integer representing the minimum required free space in megabytes.
3. Check the `HEARTBEAT_FILE`: Use the `stat` system call to find out how many seconds ago the file was last modified (compared to the current time). If the file does not exist, treat the age as `-1`.
4. Check the `DATA_DIR`: Use `statvfs` to calculate the available free space in megabytes (use `f_bavail * f_frsize / (1024 * 1024)`).
5. Determine the status: The system is "UP" if the heartbeat file exists, its modification age is less than or equal to 60 seconds, and the available free space in `DATA_DIR` is strictly greater than `MIN_SPACE_MB`. Otherwise, the status is "DOWN".
6. Append a single JSON-formatted line to `/home/user/sre_status.log` with the exact format:
   `{"status": "UP", "free_mb": 1024, "heartbeat_age_sec": 15}`
   (Replace "UP" with "DOWN" if applicable, and use the actual computed integer values).

Compile your program using `gcc` and output the executable to `/home/user/sre_monitor`.

Phase 2: Configuration and Mock Environment
1. Create the configuration file at `/home/user/monitor.conf` with the following exact contents:
   ```
   HEARTBEAT_FILE=/home/user/app_state/beat.txt
   DATA_DIR=/home/user/app_state
   MIN_SPACE_MB=5
   ```
2. Create the directory `/home/user/app_state`.
3. Create the heartbeat file `/home/user/app_state/beat.txt`.
4. Set the modification time of `/home/user/app_state/beat.txt` to exactly 30 seconds before the current system time. (You can use the `touch` command for this).

Phase 3: Execution
Run your compiled program exactly once, passing `/home/user/monitor.conf` as the argument:
`/home/user/sre_monitor /home/user/monitor.conf`

Ensure the log file `/home/user/sre_status.log` is successfully created with the correct JSON output.