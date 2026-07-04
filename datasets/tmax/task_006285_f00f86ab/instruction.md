You are acting as a network engineer troubleshooting a local service connectivity issue. We have a custom user-space UDP proxy written in C++ that is supposed to bridge traffic from our frontend simulator on port 8080 to our backend data processor on port 9090. However, the proxy is currently broken, the logs are unsecured, and the service monitoring is not configured.

You need to resolve this issue by completing the following objectives:

1. **Fix and Compile the Proxy**:
   - The source code is located at `/home/user/workspace/proxy.cpp`.
   - It contains networking bugs preventing it from listening on `127.0.0.1:8080` and forwarding to `127.0.0.1:9090`.
   - Fix the C++ code so it correctly binds to port `8080` on localhost, receives UDP packets, writes a log entry for each received packet in the exact format `FORWARDED: <packet_content>` to `/home/user/logs/proxy.log`, and then forwards the packet to port `9090` on localhost.
   - Compile the fixed code to an executable at `/home/user/workspace/proxy`.
   - Start the proxy process in the background.

2. **Configure Permissions**:
   - The directory `/home/user/logs` must be secured. Set the directory permissions so that the owner has full access (read/write/execute), but the group and others have absolutely no access (0 permissions).

3. **Schedule Monitoring**:
   - We have a monitoring script at `/home/user/workspace/monitor.sh`.
   - Install a user cron job that executes `/home/user/workspace/monitor.sh` exactly once every minute (`* * * * *`).

Ensure the proxy remains running in the background when you finish your task, as the automated tests will send test payloads to `127.0.0.1:8080` and verify the output in `/home/user/logs/proxy.log`.