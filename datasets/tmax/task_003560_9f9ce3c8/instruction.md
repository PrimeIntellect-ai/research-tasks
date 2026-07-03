You are a FinOps analyst tasked with automating the aggregation of cloud cost data and exposing it securely to an internal dashboarding tool via a local forward. 

Your task is to set up the data aggregation pipeline, configure strict permissions, and expose the results via a port-forwarded background service.

Please complete the following steps:

1. **Write the Aggregation Script**: 
   Create a Python script at `/home/user/generate_report.py`. This script must read two existing JSON files: `/home/user/aws_cost.json` and `/home/user/gcp_cost.json`. Each file contains a JSON object with a single key `"cost"` (e.g., `{"cost": 100.50}`). 
   The script must calculate the sum of these two costs and write a new JSON object to `/home/user/reports/summary.json` in the exact format: `{"total_cost": <sum>}`.

2. **Run the Script & Set Permissions**:
   Create the `/home/user/reports` directory if it does not exist. Run your `generate_report.py` script so that `summary.json` is generated.
   To ensure data compliance, change the file permissions of `/home/user/reports/summary.json` so that it is strictly read-only for the owner, with no permissions for group or others (i.e., `0400`).

3. **Manage the Reporting Service**:
   Start a simple Python HTTP server in the background that serves *only* the contents of the `/home/user/reports` directory on port `8080`. 
   Save the exact Process ID (PID) of this background HTTP server to a file located at `/home/user/server.pid`.

4. **Configure Port Forwarding**:
   The dashboarding tool expects to connect to port `9090`. Use `socat` (or another port forwarding tool) to set up a local port forward so that any TCP traffic sent to `127.0.0.1:9090` is forwarded to `127.0.0.1:8080`.
   Run this forwarding process in the background and save its PID to `/home/user/tunnel.pid`.

Ensure all background processes are running and the files are accurately placed and permissions are set before concluding your work.