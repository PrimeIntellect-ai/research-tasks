You are an edge computing engineer configuring an IoT gateway on a remote, unprivileged Linux node. You need to prepare the directory structure for telemetry data, set up a user-space port forward for a localized data ingestion service, and create a diagnostic script to verify connectivity. 

Perform the following tasks:

1. **Directory and Link Management:**
   - Create the directory path: `/home/user/iot_gateway/telemetry/node_01`.
   - Create a symbolic link at `/home/user/iot_gateway/current_node` that points to the `/home/user/iot_gateway/telemetry/node_01` directory.

2. **User-Space Port Forwarding:**
   - The IoT gateway software expects telemetry on port `8443`, but the internal ingestion service will run on port `9443`.
   - Use `socat` to create a TCP port forward: listen on port `8443` (all interfaces or localhost) and forward traffic to `127.0.0.1:9443`. 
   - Run this `socat` process in the background so it continues running.

3. **Connectivity Diagnostics Script:**
   - Write a Bash script at `/home/user/iot_gateway/diagnostics.sh`.
   - The script must check if local port `8443` is accepting connections (you may use `nc` or bash's `/dev/tcp`).
   - If the port is reachable, the script must append the exact string `OK_FORWARDING` to `/home/user/iot_gateway/health.log`.
   - Ensure the script is executable.

4. **Execution and Permissions:**
   - Run the script you just created so that `/home/user/iot_gateway/health.log` is populated.
   - Set the file permissions of `/home/user/iot_gateway/health.log` to exactly `644` (read/write for owner, read for group and others) to simulate standard service account access limits.