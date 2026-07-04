You are a Site Reliability Engineer (SRE). Our custom uptime monitoring service, "UptimeTracker", recently crashed and failed to restart. The on-call alerts are firing, and you need to get the service running again immediately.

The system components are located in `/home/user/app` and `/home/user/data`:
- `/home/user/app/main.go`: The main Go application that processes the monitoring logs.
- `/home/user/app/run.sh`: The startup script used by our process manager.
- `/home/user/data/tracker.wal`: A Write-Ahead Log (WAL) containing recent ping events formatted as JSON lines.
- `/home/user/data/config.json`: A dummy configuration file.

The application is supposed to read the WAL, process the events, and generate a summary report at `/home/user/app/uptime_report.json`. However, several issues are causing it to crash:
1. An environment misconfiguration is preventing the app from finding its config file.
2. The application is panicking due to an off-by-one error during state calculation.
3. The Base64 encoded URLs in the WAL are not decoding correctly due to an encoding mismatch.
4. A recent crash left a corrupted (truncated) JSON entry at the end of the WAL, preventing recovery. The application should gracefully skip corrupted WAL entries rather than crashing.

Your task:
1. Investigate and fix the errors in `/home/user/app/run.sh` and `/home/user/app/main.go`.
2. Ensure the application successfully parses all valid lines in `/home/user/data/tracker.wal` while skipping any corrupted lines.
3. Run the application so that it successfully generates `/home/user/app/uptime_report.json`.

The final `uptime_report.json` must exactly match the struct serialized at the end of `main.go`, representing the total number of valid entries processed and the total number of "up" statuses.