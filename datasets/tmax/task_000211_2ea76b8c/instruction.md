You are a capacity planner building a resilient resource utilization logger. Your goal is to write, compile, and deploy a C++ monitoring daemon managed by a custom bash process supervisor, properly configured for localized timezone reporting and strict access controls.

Perform the following tasks:

1. **Workspace and Permissions:**
   - Create a directory at `/home/user/capacity_data`.
   - Create an empty log file at `/home/user/capacity_data/metrics.log`.
   - Using Access Control Lists (ACLs), grant the user `nobody` explicit read-only access to `/home/user/capacity_data/metrics.log`. Ensure the owning user retains read/write access.

2. **C++ Monitoring Daemon:**
   - Write a C++ program at `/home/user/monitor/cap_monitor.cpp`.
   - The program must take exactly two command-line arguments: `interface_name` and `gateway_ip`.
   - It should read the 1-minute load average from `/proc/loadavg`.
   - Every 1 second, it must append a single line to `/home/user/capacity_data/metrics.log` in exactly this format:
     `[YYYY-MM-DD HH:MM:SS] IFACE:<interface_name> GW:<gateway_ip> LOAD:<1-min-load>`
     *(Note: The time must be the current local time of the process, formatted as a 24-hour clock).*
   - Compile the program to an executable named `/home/user/monitor/cap_monitor`.

3. **Routing Configuration and Process Supervision:**
   - Write a bash supervisor script at `/home/user/monitor/supervise.sh`.
   - The script must dynamically determine the system's default network interface and default gateway IP address (e.g., by parsing the output of `ip route`).
   - The script must export the `TZ` environment variable set to `Asia/Tokyo` so the C++ program logs time in Japan Standard Time (JST).
   - The script must run `/home/user/monitor/cap_monitor` in a continuous loop, passing the discovered default interface and gateway IP as arguments. If the C++ executable crashes or is killed, the supervisor must immediately restart it.

4. **Execution:**
   - Start your supervisor script in the background (`nohup` or `&`) so it begins logging.
   - Leave the supervisor running. Wait a few seconds to ensure at least 3 lines have been successfully written to `/home/user/capacity_data/metrics.log`.