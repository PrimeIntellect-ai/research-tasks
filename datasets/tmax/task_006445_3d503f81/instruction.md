You are an observability engineer tuning the local data ingestion for our dashboards. We have a legacy metrics exporter called `telemetry-cli` that feeds data to our dashboard system. Unfortunately, it requires an interactive login, and it is extremely sensitive to locale and timezone settings.

Your task is to automate the startup and monitoring of this telemetry feed. 

Here are the requirements:
1. The `telemetry-cli` executable is located at `/home/user/bin/telemetry-cli`. When run, it interactively prompts for a password: `Enter telemetry password: `.
2. Write an `expect` script at `/home/user/dashboard/login.exp` that launches `/home/user/bin/telemetry-cli`, waits for the password prompt, provides the password `obsv-dash-2024`, and then allows the process to continue running (do not let the expect script exit immediately; let it wait for EOF or interact so the child process stays alive).
3. Write a Bash script at `/home/user/dashboard/start_feed.sh` that does the following:
   - Sets the timezone variable `TZ` to `UTC`.
   - Sets the locale variable `LC_ALL` to `en_US.UTF-8`.
   - Sets the dashboard URL variable `METRICS_DASHBOARD_URL` to `http://localhost:9090/api/push`.
   - Executes the `/home/user/dashboard/login.exp` script with these environment variables exported.
   - Runs the expect process in the background.
   - Redirects all standard output and standard error from the expect script to `/home/user/dashboard/feed.log`.
   - Saves the exact Process ID (PID) of the backgrounded `expect` process into `/home/user/dashboard/feed.pid`.
4. Make sure your scripts are executable.
5. Execute `/home/user/dashboard/start_feed.sh` so the telemetry feed is actively running in the background.

The final state must have the `start_feed.sh` script successfully executed, the `expect` process running in the background, the correct PID written to `feed.pid`, and `feed.log` populated with the output of the `telemetry-cli` process.