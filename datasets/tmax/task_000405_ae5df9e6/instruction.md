You are acting as a FinOps analyst trying to optimize cloud costs. Our cloud provider charges excessively for per-endpoint health checks and external load balancers. To reduce costs, we want to consolidate our internal service health checks into a single lightweight agent and handle traffic routing locally.

Your task is to write a C++ health-monitoring utility, along with a deployment script that automates diagnostics, health logging, and local port forwarding.

Step 1: Create the C++ Health Checker
Write a C++ program at `/home/user/finops_health_check.cpp`.
This program must:
- Accept exactly one command-line argument: the absolute path to a configuration file containing a list of endpoints.
- The configuration file will contain one endpoint per line in the format `hostname:port` (e.g., `127.0.0.1:9001`).
- The program must attempt a standard TCP socket connection to every endpoint listed in the file.
- If it successfully connects to *all* endpoints, it must print exactly `ALL_UP` to standard output and exit with code 0.
- If it fails to connect to *any* endpoint, it must print exactly `DOWN_REASON: <hostname>:<port>` for the first endpoint that failed, and exit with code 1.

Step 2: Create the Automation and Forwarding Script
Write a bash script at `/home/user/deploy_finops.sh`. Ensure it has execute permissions.
When run, this script must:
1. Compile `/home/user/finops_health_check.cpp` into an executable named `/home/user/finops_health_check` using `g++`.
2. Set up local port forwarding to bypass the expensive cloud load balancer. Use `socat` to listen on TCP port `8080` and forward all traffic to TCP port `8081`. This `socat` process must run in the background.
3. Start a continuous background monitoring loop that executes `/home/user/finops_health_check` against the configuration file `/home/user/services.conf` every 2 seconds.
4. If the C++ executable exits with code 0 (success), the loop must append exactly the line `CLOUD_HEALTH: PASS` to `/home/user/cloud_health.log`.
5. If the C++ executable exits with a non-zero code (failure), the loop must append exactly the line `CLOUD_HEALTH: FAIL` to `/home/user/cloud_health.log`.

Note: 
- You must write the C++ code to handle basic TCP socket creation, connection, and cleanup.
- `/home/user/services.conf` will be created by our testing environment.
- Do not stop or block the terminal; ensure the script backgrounds the long-running processes (the `socat` forwarder and the monitoring loop) so that the script returns.