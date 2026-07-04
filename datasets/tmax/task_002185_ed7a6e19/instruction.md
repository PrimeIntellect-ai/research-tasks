You are acting as a network engineer tasked with fixing a broken user-space connection monitoring system. The system consists of a dummy network service, a process supervisor, and a routing configuration file. 

Your task involves three parts:

1. **Log Rotation**: The dummy service logs to `/home/user/monitor/network.log`. This file grows rapidly and needs rotation. Write a Bash script at `/home/user/scripts/log-rotator.sh` that checks the size of `/home/user/monitor/network.log` in lines. If the file has strictly more than 50 lines, it must rotate the logs. 
    - You must keep up to 3 old versions: `network.log.1`, `network.log.2`, and `network.log.3`.
    - `network.log.1` should be the most recently rotated log.
    - When rotation occurs, the original `network.log` should be emptied (truncated), not deleted, to preserve potential file descriptors.
    - Ensure your script handles cases where older log files (like `.2` or `.3`) do not exist yet.
    - Make sure the script is executable.

2. **Process Supervision**: The current supervisor script at `/home/user/scripts/net-monitor.sh` is incomplete. It only checks the status of the service once and exits.
    - Modify `/home/user/scripts/net-monitor.sh` so that it runs in an infinite loop, checking the status every 1 second.
    - It must check if the script `/home/user/scripts/dummy-service.sh` is running (you can use `pgrep -f "dummy-service.sh"`).
    - If the service is NOT running, your monitor script must start it in the background (`/home/user/scripts/dummy-service.sh &`) and echo "Restarted dummy-service" to stdout.

3. **Routing Configuration Parsing**: You have a corrupted routing file at `/home/user/config/routes.conf`. 
    - Parse this file and extract only the valid routes. 
    - A valid route line consists of exactly three space-separated fields: `Destination Gateway Interface`.
    - `Destination` and `Gateway` must be valid IPv4 addresses (or `0.0.0.0`). You can assume any string of four dot-separated numbers is structurally close enough to an IP for this exercise, as long as it doesn't contain letters.
    - `Interface` MUST start with either `eth` or `tun`.
    - Save all valid route lines (exactly as they appear) to `/home/user/config/active_routes.txt`.

Ensure all required scripts are executable. Do not start the monitor script yourself in a permanent background process; the automated tests will execute your scripts to verify them.