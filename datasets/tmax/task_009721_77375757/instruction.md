You are a FinOps analyst tasked with optimizing local testing infrastructure to reduce cloud costs. Your developers use a set of local mock APIs to avoid hitting expensive cloud endpoints during testing. However, due to a network misconfiguration, the mock services are unreachable, causing the application to fail over to the expensive cloud endpoints automatically. 

Your objective is to fix the routing, establish port forwarding for the hardcoded legacy application, and implement a Bash-based cost-optimization scheduler.

Complete the following phases:

**Phase 1: Reverse Proxy & Load Balancer Setup**
We need to load balance traffic across three local mock service instances.
1. Create an HAProxy configuration file at `/home/user/haproxy.cfg`.
2. Configure a `frontend` named `app_front` listening on `127.0.0.1:8080`.
3. Configure a `backend` named `mock_pool` that uses round-robin load balancing.
4. Add three local mock servers to the backend pool:
   - `mock1` at `127.0.0.1:8081`
   - `mock2` at `127.0.0.1:8082`
   - `mock3` at `127.0.0.1:8083`
5. Add a fallback/backup server named `cloud_api` to the same backend pool at `127.0.0.1:8084`. This server must ONLY be used if `mock1`, `mock2`, and `mock3` are all down.
6. Start the `haproxy` process in the background using your configuration file.

**Phase 2: Port Forwarding for Legacy Application**
The legacy application is hardcoded to send requests to `127.0.0.1:9000`. 
1. Create a Bash script at `/home/user/forwarder.sh`.
2. In this script, use `socat` to forward all TCP traffic from `127.0.0.1:9000` to your HAProxy frontend at `127.0.0.1:8080`.
3. Make the script executable and ensure it runs in the background.

**Phase 3: Cost Optimization Scheduled Task**
To save compute resources, we want to scale down services when usage is low. Since we don't have root access for `cron`, we will use a continuous background script.
1. Create a Bash script at `/home/user/cost_optimizer.sh`.
2. The script should run an infinite loop, pausing for 2 seconds between iterations.
3. In each iteration, it must read the contents of `/home/user/usage.txt`.
4. If the file contains exactly the string `STATUS=IDLE`, the script must append the exact line `FinOps: Scaled down mock3` to `/home/user/scaling.log`.
5. Run this script in the background.

*Note: For testing purposes, you can assume the mock servers on 8081-8084 are managed externally. You only need to set up HAProxy, the socat forwarder, and the optimizer script.*