You are acting as a capacity planner and system administrator. We are simulating a microservice environment locally to analyze resource usage and test our load balancing setup. 

Currently, our backend services cannot be reached correctly through the reverse proxy due to network misconfigurations in our startup scripts and proxy config.

Your task is to fix the backend deployment, configure the load balancer, and set up a scheduled capacity monitoring script.

Please complete the following steps:

1. **Fix Backend Services:**
   There is a script located at `/home/user/capacity_planner/start_backends.sh` that is supposed to start three lightweight backend services (Python HTTP servers) on `127.0.0.1`. They must run on ports `8081`, `8082`, and `8083`. Currently, the script has typos and misconfigurations causing some nodes to fail or bind to the wrong ports. 
   - Fix `/home/user/capacity_planner/start_backends.sh` so it correctly starts all three servers in the background.
   - Execute the script so the services are running.

2. **Configure Load Balancer:**
   We are using HAProxy as our reverse proxy. The configuration file is at `/home/user/capacity_planner/haproxy.cfg`.
   - Update the configuration so the frontend listens on `127.0.0.1:8080`.
   - Update the backend pool to correctly load balance across the three backend nodes (`127.0.0.1:8081`, `127.0.0.1:8082`, and `127.0.0.1:8083`).
   - Start HAProxy in the background as the current user using this configuration.

3. **Create a Capacity Monitor:**
   Create a bash script at `/home/user/capacity_planner/check_capacity.sh` that does the following:
   - Uses `curl` in silent mode to make a GET request to `http://127.0.0.1:8080/`.
   - Appends the raw response body, followed by a newline, to `/home/user/capacity_planner/capacity_log.txt`.
   Make sure the script is executable. Run the script manually exactly once to seed the log file.

4. **Schedule the Monitor:**
   Since we don't have access to the global cron daemon, write a valid crontab line into a new file at `/home/user/capacity_planner/crontab.txt`. The line should schedule `/home/user/capacity_planner/check_capacity.sh` to run exactly every 5 minutes.

Ensure all running processes (HAProxy and Python servers) remain running in the background when you finish.