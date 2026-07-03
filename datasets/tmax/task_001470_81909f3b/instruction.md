You are a Site Reliability Engineer tasked with automating the startup and monitoring of a legacy interactive API server. You must operate entirely within the `/home/user` directory without root privileges.

The legacy backend server is located at `/home/user/legacy_api.sh`. It is an interactive bash script that cannot be modified. When run, it asks for a passcode and a confirmation before starting an HTTP server on port 9000.

Your task is to integrate this into a reliable setup by completing the following steps:

1. **Automate Startup with Expect**: Write an `expect` script at `/home/user/start_api.exp` that automates the execution of `/home/user/legacy_api.sh`. 
   - It must wait for the prompt `"Enter SRE passcode: "` and send `"SRE-8891"`.
   - It must wait for the prompt `"Start server? (y/n): "` and send `"y"`.
   - It must allow the underlying server process to keep running (do not let the expect script exit immediately and kill the child process; use `interact` or an appropriate wait).

2. **Reverse Proxy Configuration**: We need a reverse proxy in front of this API. Create an HAProxy configuration file at `/home/user/haproxy.cfg` that:
   - Runs in the foreground/unprivileged (no global `daemon` or `user/group` settings that require root).
   - Configures a `frontend` listening on `127.0.0.1:8080`.
   - Routes traffic to a `backend` pointing to `127.0.0.1:9000`.

3. **Uptime Monitoring Script**: Write a robust bash script at `/home/user/monitor.sh` that checks the health of the reverse proxy.
   - The script must use `curl` to silently fetch `http://127.0.0.1:8080/` with a maximum timeout of 2 seconds.
   - If the `curl` command succeeds (exit code 0), append the exact string `UP` to `/home/user/uptime.log`.
   - If the `curl` command fails, append the exact string `DOWN` to `/home/user/uptime.log`.
   - Make sure `/home/user/monitor.sh` is executable.

4. **Scheduled Task**: We need this monitor to run every 5 minutes. Since you do not have root access to modify the system cron daemon directly, write the standard crontab line that would achieve this (running `/home/user/monitor.sh` every 5 minutes) into a text file named `/home/user/crontab.txt`.

Ensure all files are created exactly at the specified paths. Do not start the HAProxy or the Expect script in the background; the automated test will invoke your scripts and configurations to verify them.