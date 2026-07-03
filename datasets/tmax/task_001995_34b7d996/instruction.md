You are a network security engineer investigating a potential rogue service on a local testing server. 

Several background services are running on this machine (written in Python and Node.js). You have been provided with a network access log located at `/home/user/traffic.log`.

Your objectives are:

1. **Service Auditing:** Identify the local port being used by the running `node` service. There are multiple background services, but only one is running via Node.js.
2. **Log Parsing and Correlation:** Analyze the `/home/user/traffic.log` file. The log entries follow this format:
   `[YYYY-MM-DD HH:MM:SS] SRC_IP:SRC_PORT -> 127.0.0.1:LOCAL_PORT HTTP_METHOD /PATH`
   Correlate the Node.js service's local port with the incoming traffic. Find the source IP address that has made the most requests to this specific Node.js service.
3. **Reporting:** Write the identified source IP address into a file named `/home/user/rogue_ip.txt`. The file should contain *only* the IP address.
4. **Process Isolation (Sandboxing):** To prevent future services from communicating with unauthorized external networks, create a reusable sandbox wrapper script at `/home/user/secure_run.sh`. 
   - The script must take a command as its arguments and run that command using `bwrap` (Bubblewrap).
   - The sandbox must share the host filesystem (read/write as appropriate, e.g., `--bind / /`) so the command can execute normally.
   - The sandbox **must isolate the network** (using the appropriate bwrap flag) so that the running command cannot access external networks (only loopback/isolated networking).
   - The script must be executable.

Ensure your wrapper script works correctly. If an automated test runs `/home/user/secure_run.sh ip link`, it should only see the loopback interface, not the standard eth0 network interface.