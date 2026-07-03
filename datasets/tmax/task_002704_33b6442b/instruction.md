You are a FinOps analyst tasked with optimizing cloud costs for a legacy system. We are charged heavily for invalid traffic hitting our backend service and for excessive log storage. 

To solve this, you need to implement an application-level proxy/firewall in C++, configure log rotation, and write a staged deployment script.

Step 1: The C++ Proxy (Application Firewall)
Write a C++ program at `/home/user/proxy.cpp`. This program should simulate a proxy that filters traffic before it reaches the backend.
- It must read a single line of input from `stdin`.
- If the line starts exactly with the string `"COST"`, it should print `"FORWARD"` to `stdout` (simulating forwarding to the backend).
- If the line does NOT start with `"COST"`, it should print `"DROP"` to `stdout`, and append the log entry `[BLOCKED] <input_line>` followed by a newline to `/home/user/proxy.log`.

Step 2: Log Rotation Configuration
Logs are expensive to store. Create a user-space logrotate configuration file at `/home/user/logrotate.conf` that manages `/home/user/proxy.log`.
- It should rotate the log `daily`.
- It should keep exactly `2` rotations (`rotate 2`).
- Rotated logs must be compressed (`compress`).
- It should not produce an error if the log file is missing (`missingok`).

Step 3: Staged Deployment Script
We currently have a dummy active binary at `/home/user/proxy_active`.
Create a bash script at `/home/user/deploy.sh` (ensure it is executable) that performs a staged deployment of your new proxy:
1. Compiles `/home/user/proxy.cpp` into a new binary named `/home/user/proxy_v2`.
2. Backs up the current active proxy by moving `/home/user/proxy_active` to `/home/user/proxy_backup`.
3. Creates a symbolic link at `/home/user/proxy_active` that points to the newly compiled `/home/user/proxy_v2`.

Ensure all file paths are exact as specified above.