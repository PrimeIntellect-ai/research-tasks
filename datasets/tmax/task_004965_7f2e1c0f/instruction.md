You are an observability engineer tuning the dashboard backend for a storage monitoring system. 

We have a C++ backend agent that is supposed to report the disk space metrics of the `/home/user/app_data` directory. Currently, there is a bug in the C++ code, and the infrastructure is not fully deployed.

Your objectives:

1. **Fix and Compile the Backend:**
   Inspect the C++ source file located at `/home/user/metrics_agent.cpp`. It is designed to serve a JSON response with the disk metrics on a port specified via command line arguments. Fix the bug where it incorrectly calculates the available space (it currently hardcodes a value). Use `std::filesystem::space` to correctly determine the *available* bytes on the filesystem where `/home/user/app_data` resides.
   Compile the fixed code to an executable named `/home/user/metrics_agent`.

2. **Staged Deployment:**
   Deploy three instances of this metrics agent running in the background on ports `8081`, `8082`, and `8083`. 

3. **Reverse Proxy / Load Balancer:**
   Create an HAProxy configuration file at `/home/user/haproxy.cfg` that listens on port `8080` and distributes HTTP requests round-robin to the three backend instances (`127.0.0.1:8081`, `127.0.0.1:8082`, `127.0.0.1:8083`). Start HAProxy in the background using this configuration.

4. **Port Forwarding via SSH:**
   The dashboard UI expects to connect to port `9090`. Establish a local SSH tunnel that forwards local port `9090` to `localhost:8080`. Run this tunnel in the background. (Passwordless SSH to `user@localhost` has already been set up for you).

5. **Verification:**
   Write a bash script at `/home/user/poll_metrics.sh` that makes exactly 6 HTTP GET requests to `http://localhost:9090` using `curl` (suppress progress output), separated by a 1-second `sleep`. The script should append the raw JSON responses to `/home/user/dashboard_metrics.log`, each on a new line. Execute the script to populate the log file.

Constraints:
- Do not use root/sudo. 
- Ensure all background processes are running and the `.log` file is successfully generated.