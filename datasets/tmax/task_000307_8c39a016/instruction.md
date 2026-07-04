You are an infrastructure engineer automating the provisioning of a lightweight microservice environment. Since you do not have root access, you will build user-space scripts that handle application deployment, user-space port forwarding (simulating NAT), and log-based threat mitigation.

Write a bash script at `/home/user/deploy.sh` that performs the following tasks idempotently. You will also need to write a simple Python application as part of the deployment.

**Phase 1: Microservice Application**
Write a Python web server script at `/home/user/app.py`. 
- It must listen on `127.0.0.1` port `8080`.
- It must respond to any `GET` request with the exact HTTP 200 text response: `Deploy Success`
- The `deploy.sh` script must start this application in the background (e.g., using `nohup` or `&`).
- **Idempotency Requirement:** Your `deploy.sh` must check if the application is already running on port 8080. If it is, do not start a new instance.

**Phase 2: User-Space Port Forwarding**
Since we cannot use `iptables`, we will simulate a firewall/NAT rule using `socat`.
- The `deploy.sh` script must use `socat` to forward TCP traffic from `127.0.0.1` port `9090` to `127.0.0.1` port `8080`.
- **Idempotency Requirement:** The script must check if a port forward is already active on port `9090`. If it is, do not start a new `socat` process. Start it in the background if it is not running.

**Phase 3: Log Processing Pipeline**
An existing log file is located at `/home/user/historical.log`. The file contains logs in the format:
`[YYYY-MM-DD HH:MM:SS] LEVEL IP_ADDRESS METHOD PATH STATUS_CODE`

Your `deploy.sh` script must use text processing tools (`awk`, `sed`, `grep`, etc.) to:
1. Find all log entries that have a `404` status code.
2. Extract the IP addresses associated with these 404 errors.
3. Count the number of 404 errors per IP address.
4. Output the top 3 IP addresses with the highest number of 404 errors (sorted in descending order of count, then ascending order of IP address if there is a tie) to `/home/user/blocked_ips.txt`.
- The format for `/home/user/blocked_ips.txt` must be exactly: `<IP_ADDRESS> <COUNT>` (e.g., `192.168.1.100 15`).

**Phase 4: Mock Firewall Configuration**
Finally, `deploy.sh` must generate a mock firewall configuration file at `/home/user/firewall.conf`.
- For each IP address in `/home/user/blocked_ips.txt`, append a line to `/home/user/firewall.conf` in the format: `DENY_IP <IP_ADDRESS>`
- Ensure that the file is created from scratch each time the script is run, so it only contains the currently blocked IPs.

Ensure `/home/user/deploy.sh` is executable and run it at least once so the services are running and the output files are generated.