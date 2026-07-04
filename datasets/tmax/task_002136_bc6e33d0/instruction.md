I am a monitoring specialist setting up a fast local alerting system, but I'm running into deployment and performance issues with our vendored monitoring package. 

We have a vendored package located at `/app/port-monitor-1.0`. It contains a `Makefile` and a bash script `port-monitor.sh`. The script reads a list of local ports from a file and checks if they are accepting connections. If a port is down, it logs an alert.

I need you to do the following:
1. **Fix the Installation**: The `Makefile` is currently configured to install the script to `/usr/local/bin`, but you do not have root access. Modify the `Makefile` to install the executable to `/home/user/bin/` instead, and run `make install`.
2. **Optimize the Script**: The current `port-monitor.sh` checks ports sequentially using `nc` with a 1-second timeout. If many ports are down, it takes far too long. Rewrite or optimize `/home/user/bin/port-monitor.sh` (using pure Bash, `nc`, or coreutils) so that it processes the ports concurrently or with extreme efficiency. It must output lines in the exact format `Port <port_number> is DOWN` to the log file for every port that refuses a connection.
3. **Service Configuration**: Create a user-level systemd service file at `/home/user/.config/systemd/user/port-monitor.service`. The service should execute `/home/user/bin/port-monitor.sh /home/user/ports.txt /home/user/alerts.log`. (You do not need to start the service, just create the valid unit file).

**Requirements:**
- Ensure `/home/user/bin` exists and is in the PATH.
- The optimized script must accurately identify down ports.
- The execution time of your optimized script must be under 1.5 seconds when checking a list of 200 ports.