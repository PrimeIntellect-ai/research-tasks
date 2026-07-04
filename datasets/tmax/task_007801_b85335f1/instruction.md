You are acting as a cloud architect migrating a legacy data-processing pipeline to a new Linux environment. 

During the migration, you discovered a race condition: the pipeline's startup script fails because the data processor starts before the data fetcher has fully initialized and bound to its network port. Additionally, you need to implement a storage monitoring mechanism to ensure the fetched data doesn't exceed our strict local storage quotas.

You need to perform the following three tasks:

1. **Fix the startup script:**
   There is a script located at `/home/user/start_pipeline.sh`. It currently attempts to start `/home/user/fetcher.sh` and `/home/user/processor.sh`. 
   Modify `/home/user/start_pipeline.sh` so that it:
   - Starts `/home/user/fetcher.sh` in the background.
   - Actively polls/waits until a service is listening on `127.0.0.1` port `8888` (you can use standard CLI tools like `nc`, `curl`, or bash `/dev/tcp`).
   - Once the port is open and accepting connections, starts `/home/user/processor.sh` in the background.
   - Writes the Process IDs (PIDs) of these two background processes to `/home/user/pipeline.pids`. The fetcher's PID must be on the first line, and the processor's PID must be on the second line.

2. **Create a storage monitoring script:**
   Write a bash script at `/home/user/disk_monitor.sh` that checks the total disk usage (in bytes) of the directory `/home/user/migration_data/`. 
   - If the total size of the directory and its contents is strictly greater than `1000000` bytes, the script must overwrite `/home/user/monitor_alert.log` with the exact text `QUOTA_EXCEEDED`.
   - If the size is `1000000` bytes or less, it must overwrite `/home/user/monitor_alert.log` with the exact text `OK`.
   - Make sure your script is executable.

3. **Schedule the monitoring script:**
   Install a user-level cron job (using `crontab`) that executes `/home/user/disk_monitor.sh` every minute (`* * * * *`).

Ensure all files are created exactly at the specified paths. You can verify your `start_pipeline.sh` script by running it; if successful, the processor will eventually create a file indicating success.