You are a backup operator testing a restore of an internal health-monitoring daemon. During the restore process into the test environment, you discovered that the daemon cannot reach the local backup verification service due to a network misconfiguration embedded in the code.

The restored files are located in `/home/user/restore/`:
1. `health_monitor.c` - The source code for the health monitoring daemon. It acts as a lightweight web server that reports the status of the backup verification service.
2. `send_alert.sh` - A mock email alerting script used by the daemon.
3. `backup_service.py` - A dummy python service simulating the backup verification endpoint.

Your task is to fix and deploy the restored monitoring daemon:
1. The `backup_service.py` is already running on `127.0.0.1` port `9090` (you do not need to start it).
2. Inspect `health_monitor.c`. It contains a hardcoded IP address `192.0.2.100` for the backup service, which simulates a broken Docker network route in our restore environment. Modify the C code to point to the correct local IP address (`127.0.0.1`).
3. Compile the C code into an executable named `monitor_daemon` in the `/home/user/restore/` directory. (You can use `gcc`).
4. The daemon requires two environment variables to run correctly:
   - `HEALTH_PORT`: Set this to `8080`.
   - `ALERT_SCRIPT`: Set this to the absolute path `/home/user/restore/send_alert.sh`.
5. Start your compiled `monitor_daemon` in the background.
6. Once the daemon is running, it will host a health check endpoint. Make an HTTP GET request to `http://127.0.0.1:8080/status` using `curl`.
7. Save the exact response from the `curl` command into `/home/user/health_report.log`.

Do not modify `send_alert.sh` or `backup_service.py`. Ensure your final output is written to `/home/user/health_report.log`.