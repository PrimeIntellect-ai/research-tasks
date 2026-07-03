A network engineer at your company has written a small Go script to monitor local network connectivity, specifically checking if port 8080 is reachable. They have configured a custom scheduler to execute this monitoring script every minute. 

However, they are running into a few issues due to the stripped-down environment of the scheduler (similar to a cron job):
1. The scheduler runs the wrapper script (`/home/user/netmon/run.sh`) with a completely empty environment (as if invoked via `env -i`). As a result, the `go` command fails to run because it cannot find its binaries, and it complains about missing cache directories (`GOCACHE` / `HOME`).
2. The log files are currently being dumped into `/tmp/status.log` instead of the persistent logging directory because an environment variable is missing.
3. The directory meant to hold the persistent logs needs strict permissions for compliance.

Your task is to fix the wrapper script and the Go program:

1. **Fix the Go script**: The script is located at `/home/user/netmon/monitor.go`. It currently hardcodes its output path to `/tmp/status.log`. Modify the Go script so that it reads the environment variable `NET_LOG_DIR`. If `NET_LOG_DIR` is set, it should write the log to `status.log` inside that directory. If the variable is empty or unset, it should fall back to `/tmp/status.log`.
2. **Fix the wrapper script**: Edit `/home/user/netmon/run.sh`. You must add the necessary environment variables to allow `go run /home/user/netmon/monitor.go` to execute successfully from a completely empty environment. You will need to set:
   - `PATH` (ensure it includes standard system binary paths and the Go binary path).
   - `HOME` (set to `/home/user`) or `GOCACHE` (set to `/home/user/.cache/go-build`) so the Go compiler has a valid temporary build directory.
   - `NET_LOG_DIR` set to `/home/user/net_logs`.
3. **Configure Permissions**: Within `/home/user/netmon/run.sh`, before executing the Go script, ensure that the directory `/home/user/net_logs` is created and that its permissions are set exactly to `750`.
4. **Test it**: Simulate the scheduler by running the wrapper script with an empty environment: `env -i bash /home/user/netmon/run.sh`. 

Verify your work by ensuring that `/home/user/net_logs/status.log` is successfully created and contains the network status output (which should read `STATUS: 8080_CLOSED` if nothing is listening on port 8080).