You are a Site Reliability Engineer (SRE) managing a simple text-based configuration for a custom load balancer. Recently, some backend services have been failing, causing network misconfigurations where the load balancer routes traffic to dead endpoints.

Your task is to create a Bash automation script that acts as an active health monitor, performs connectivity diagnostics, and automatically updates the reverse proxy configuration.

Perform the following steps exactly as described:

1. **Setup the Environment:**
   Create a directory `/home/user/lb/` and inside it, create a file named `backends.list` with the exact following contents:
   ```text
   server backend_A 127.0.0.1:8001
   server backend_B 127.0.0.1:8002
   server backend_C 127.0.0.1:8003
   ```

2. **Simulate the Services:**
   Using Python's built-in HTTP server, start dummy backend services on ports `8001` and `8003` in the background (e.g., `python3 -m http.server 8001 &`). 
   **Do NOT** start a service on port `8002`. This simulates a crashed backend (`backend_B`).

3. **Write the Monitoring Script:**
   Create a Bash script at `/home/user/lb/monitor.sh`. The script must perform the following tasks when executed:
   - Read the `/home/user/lb/backends.list` file line by line.
   - For each line, extract the server name and the `IP:PORT` combination.
   - Perform an HTTP GET request (connectivity diagnostic) to `http://IP:PORT/` using `curl` with a maximum timeout of 1 second.
   - Generate a new configuration file at `/home/user/lb/active.list`. 
   - If the endpoint returns a successful HTTP 200 response, write the line exactly as it appears in the original list to `/home/user/lb/active.list`.
   - If the endpoint fails to respond or times out, write the line to `/home/user/lb/active.list` but prepend it with a `# ` (a hash and a space, effectively commenting it out).
   - For every unreachable endpoint, append a log entry to `/home/user/lb/health.log` in this exact format:
     `ERROR: <server_name> on <IP:PORT> is unreachable`
     (For example: `ERROR: backend_B on 127.0.0.1:8002 is unreachable`)

4. **Execute the Script:**
   Make your script executable and run it once so that `/home/user/lb/active.list` and `/home/user/lb/health.log` are generated based on the simulated services.

Ensure all paths used in your script are absolute paths as requested.