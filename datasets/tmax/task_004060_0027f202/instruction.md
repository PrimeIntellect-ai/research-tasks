You are an SRE investigating a failing uptime monitoring system. Our custom lightweight monitoring daemon, `bash-uptime-monitor`, is failing to correctly report the status of several critical internal services and frequently corrupts its internal state dashboard. 

The source code for the monitor is vendored at `/app/bash-uptime-monitor-v2.1`. No internet access is required or allowed to fetch external packages.

You have three main objectives:
1. **Network Packet Capture Analysis**: We captured the health check traffic when the daemon attempted to probe our legacy web server. The capture is located at `/home/user/healthcheck_trace.pcap`. Analyze the pcap file using standard CLI tools (e.g., `tcpdump`). You will notice that the HTTP health checks are failing with 400 Bad Request because the bash script formats the raw HTTP GET request incorrectly (data transformation error). Find the file in the vendored package responsible for generating the HTTP probe and fix the data transformation so it sends a valid HTTP/1.1 GET request with the correct `Host` header and `\r\n\r\n` termination.
2. **Race Condition and Concurrency Debugging**: The monitor runs checks in parallel using background jobs in bash. However, it updates a shared state file `/home/user/dashboard_state.json` directly from multiple background jobs, causing intermediate state corruption (invalid JSON). Modify the monitoring logic to prevent this race condition. You may use intermediate state tracing to verify the fix, ensuring the final JSON is always strictly valid.
3. **Integration and Service Bring-up**: Once the bugs are fixed, start the monitor and its built-in dashboard.
   - You must configure the dashboard to listen on exactly `127.0.0.1:8080`.
   - The dashboard script `serve.sh` requires an authentication token to be set via the `ADMIN_TOKEN` environment variable. Set it to `sre-secret-77x`.
   - Run the service in the background so it remains active.

Leave the service running on port 8080. The automated verification system will issue requests to the dashboard to confirm it reports the targets correctly without state corruption.