You are a Site Reliability Engineer tasked with setting up an automated health check and remediation script for a legacy containerized authentication service. 

Recently, the configuration for this service was accidentally modified so that it silently rejects all automated health-check probes and key-based logins. It now only responds to an interactive TCP login prompt. 

You need to create a monitoring solution that automates this interactive login to verify the service is healthy, and restarts the service if it is unresponsive or rejects the login.

Here is the environment and your requirements:

1. **The Service**: 
   - A mock authentication daemon is managed via a control script located at `/home/user/service_ctl.sh`. 
   - You can use `/home/user/service_ctl.sh start`, `stop`, `status`, or `restart`.
   - When running, the service listens on `127.0.0.1` port `8022`.

2. **The Interactive Prompt**:
   - When you connect to the service (e.g., via `nc 127.0.0.1 8022`), it will output exactly: `User: `
   - After providing the username, it will output exactly: `Pass: `
   - The correct credentials are Username: `sre_admin` and Password: `KeepAlive42!`
   - If authentication is successful, the service will output `AUTH_SUCCESS: System Healthy` and close the connection. 
   - If it fails, it will output `AUTH_FAILED` or simply drop the connection.

3. **Task 1: The Expect Script**
   - Write an `expect` script at `/home/user/healthcheck.exp`.
   - The script must connect to `127.0.0.1 8022` using `nc`.
   - It must handle the interactive prompts automatically using the credentials provided above.
   - It must exit with status code `0` if it sees `AUTH_SUCCESS: System Healthy`, and exit with status code `1` if it times out, fails to connect, or sees `AUTH_FAILED`.
   - Ensure the script is executable.

4. **Task 2: The Bash Monitor**
   - Write a Bash script at `/home/user/monitor.sh`.
   - This script must run `/home/user/healthcheck.exp`.
   - If the expect script exits with `0`, the bash script must append the exact line `STATUS: UP` to `/home/user/uptime.log`.
   - If the expect script exits with `1` (or any non-zero value), the bash script must execute `/home/user/service_ctl.sh restart` and append the exact line `STATUS: DOWN - RESTARTED` to `/home/user/uptime.log`.
   - Ensure the script is executable.

Make sure your scripts work cleanly without manual intervention. You can assume `expect` and `nc` (netcat) are installed.