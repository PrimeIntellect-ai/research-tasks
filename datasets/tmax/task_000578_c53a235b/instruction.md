You are a monitoring specialist and system administrator tasked with fixing a slow internal load balancer and setting up alerts for its backend services. 

Our internal teams use a custom-built version of a lightweight load balancer, whose source is vendored at `/app/pen-0.34.1` (the `pen` load balancer). Recently, a junior developer introduced a "rate limiting" patch directly into the C source code that has caused severe network bottlenecks between our microservices. Currently, the services can't communicate effectively due to timeouts.

Your objectives:
1. **Fix and Build the Load Balancer:**
   - Investigate the source code in `/app/pen-0.34.1`. Find the deliberate latency perturbation (a forced sleep/delay introduced in the main connection handling loop, likely `pen.c`) and remove it.
   - Compile the package from source and install the executable to `/home/user/bin/pen` (you do not have root access, so configure the installation prefix appropriately).

2. **Configure Load Balancing:**
   - Run three lightweight Python HTTP servers on ports 8001, 8002, and 8003 in the background. Each should serve a simple "OK" text response.
   - Start your compiled `pen` load balancer to listen on port 8080 and round-robin distribute TCP traffic to the three backend ports (8001, 8002, 8003).

3. **User Group Alert Monitoring (Bash):**
   - Write a Bash script at `/home/user/monitor.sh` that runs an infinite loop checking the health of the load balancer on port 8080 using `curl`.
   - If the request takes longer than 100ms or fails, the script must append a critical alert to `/home/user/alerts.log` in the format: `[YYYY-MM-DD HH:MM:SS] ALERT: LB latency high or unreachable`.
   - Start this monitoring script in the background.

The final state will be evaluated by a performance benchmarking script that verifies the load balancer's throughput and latency. You must achieve high throughput (no artificial delays) for the tests to pass. Ensure your servers and the load balancer remain running.