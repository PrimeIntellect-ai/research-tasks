You are acting as a capacity planner. You need to build a secure, local monitoring setup to analyze the resource usage of background worker processes. 

Your task involves several phases:

1. **Simulate Worker Processes:**
   Spawn exactly 3 background processes. Each process must be named `capacity-worker` (you can use `bash -c "exec -a capacity-worker sleep 3600"` or a similar technique) and run in the background.

2. **TLS Configuration:**
   Generate a self-signed ECDSA (P-256) TLS certificate and private key. Save them exactly as `/home/user/cert.pem` and `/home/user/key.pem`.

3. **Go Monitoring Server:**
   Write a Go program at `/home/user/monitor.go`. This program must:
   - Run an HTTPS web server listening strictly on `127.0.0.1:8443`.
   - Use the TLS certificate and key generated in step 2.
   - Expose a single endpoint at `/metrics`.
   - When `/metrics` is queried, the server must find all running processes named `capacity-worker`.
   - It must return a JSON response containing a list of these processes with their Process ID (PID) and Resident Set Size (RSS) memory usage in kilobytes.
   - The JSON output must strictly match this format:
     `[{"pid": 12345, "rss_kb": 1024}, {"pid": 12346, "rss_kb": 1024}, {"pid": 12347, "rss_kb": 1024}]`
   Compile and run this Go server in the background.

4. **Secure Transport via SSH Tunnel:**
   To simulate cross-network capacity planning, securely tunnel the traffic. Set up a local SSH port forwarding tunnel that forwards local port `9443` to the Go server's address (`127.0.0.1:8443`) over SSH to `localhost`. Keep this tunnel open in the background.

5. **Data Collection:**
   Write a shell script at `/home/user/fetch_metrics.sh` that:
   - Uses `curl` to query the Go server through the SSH tunnel on port `9443` (i.e., `https://127.0.0.1:9443/metrics`).
   - Ignores TLS certificate warnings (since it's self-signed).
   - Saves the exact JSON response to a file named `/home/user/capacity_report.json`.
   Execute this script so the report file is generated.

When you are finished, leave the worker processes, the Go server, and the SSH tunnel running. Ensure `/home/user/capacity_report.json` is fully populated.