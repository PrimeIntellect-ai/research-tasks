You are an observability engineer tuning dashboards and setting up resilience for a flaky local metrics visualizer. 

We have a custom mock dashboard application located at `/home/user/dash_app/dashboard.py`. Unfortunately, it has a memory leak and frequently crashes under load. Until the developers fix it, you need to set up a robust process supervisor script and fix its data source linkage.

Perform the following tasks:

1. **Directory Structure Management:**
   The dashboard expects to read metrics from `/home/user/dash_app/current_metrics`, but the data actually lives in `/home/user/metrics_data`. 
   Create a symbolic link at `/home/user/dash_app/current_metrics` that points to the target directory `/home/user/metrics_data`.

2. **Process Supervision & Health Checking:**
   Since you don't have root access to use `systemd`, write a custom Bash supervisor script at `/home/user/supervisor.sh`. The script must:
   - Make sure any existing instance of the dashboard on port 8080 is killed before starting.
   - Start the dashboard application (`python3 /home/user/dash_app/dashboard.py`) in the background.
   - Enter a continuous supervision loop that sleeps for 1 second on each iteration.
   - During each iteration, check the application's health endpoint: `http://127.0.0.1:8080/health`.
   - If the endpoint returns an HTTP status code other than 200 (or if the connection fails/times out), the supervisor must:
       a. Kill the previously tracked dashboard process.
       b. Increment a running crash counter.
       c. Restart the dashboard application in the background.
       d. Append exactly this line to `/home/user/dash_app/supervision.log`:
          `RESTART_EVENT | TOTAL_CRASHES: X` (where X is the current total crash count, starting at 1 for the first restart).

Ensure `/home/user/supervisor.sh` is executable (`chmod +x`). Do not start the script continuously yourself; just write the script and verify it works manually. An automated test will execute `/home/user/supervisor.sh` to evaluate its behavior.