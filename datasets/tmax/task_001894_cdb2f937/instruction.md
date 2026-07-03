You are acting as a capacity planner analyzing real-time storage resource usage on a Linux system. You need to implement a resilient, continuous disk-monitoring system for specific workload directories using only Bash, standard coreutils, and user-level cron. 

Your objective is to build a custom process supervision loop that ensures a monitoring script is always running, collecting data, and then perform a basic capacity analysis.

Here are your instructions:

1. **Setup Environment**:
   Ensure the following directories exist:
   - `/home/user/scripts`
   - `/home/user/logs`
   - `/home/user/workloads/db`
   - `/home/user/workloads/app`
   Create a dummy file of exactly 1MB (1048576 bytes) in `/home/user/workloads/db/init.dat` and a 2MB file in `/home/user/workloads/app/init.dat`.

2. **The Monitor Daemon (`/home/user/scripts/monitor.sh`)**:
   Write a bash script that runs an infinite loop. Every 1 second (`sleep 1`), it must:
   - Measure the total apparent size in bytes of `/home/user/workloads/db` and `/home/user/workloads/app` using `du -sb`.
   - Append this data to `/home/user/logs/usage.csv`.
   - The CSV format must be exactly: `UNIX_EPOCH_TIMESTAMP,DIRECTORY_NAME,SIZE_IN_BYTES` (e.g., `1690000000,db,1048576`). Do not include the full path in the DIRECTORY_NAME column, just `db` or `app`.

3. **The Supervisor (`/home/user/scripts/supervisor.sh`)**:
   Write a bash script that acts as a process supervisor for `monitor.sh`.
   - It must check if `monitor.sh` is currently running.
   - If it is NOT running, it must start `monitor.sh` in the background, redirecting standard error and standard out to `/dev/null`.
   - Whenever it starts the monitor, it must append a line to `/home/user/logs/supervisor.log` with the exact format: `[UNIX_EPOCH_TIMESTAMP] Restarted monitor daemon`.

4. **Scheduled Task**:
   Install a user crontab that runs `/home/user/scripts/supervisor.sh` every minute. 

5. **Execution and Capacity Event Simulation**:
   - Make your scripts executable.
   - Manually execute `/home/user/scripts/supervisor.sh` once to kick off the monitoring immediately.
   - Wait exactly 3 seconds.
   - Simulate a sudden workload spike by creating a new 5MB (5242880 bytes) file at `/home/user/workloads/db/spike.dat`.
   - Wait exactly 3 more seconds.

6. **Analysis (`/home/user/scripts/analyze.sh`)**:
   Write and execute a script that reads `/home/user/logs/usage.csv` and calculates the total growth (Maximum Size - Minimum Size) for both `db` and `app` directories.
   Output the results to `/home/user/report.txt` in the following format:
   ```
   db_growth_bytes: <value>
   app_growth_bytes: <value>
   ```

Ensure all scripts are fully autonomous and require no interactive prompts.