You are a deployment engineer tasked with fixing a botched rollout of an internal application stack ("AppStack") located in `/home/user/appstack`. The application currently returns a 502 Bad Gateway error because the proxy cannot connect to the backend's Unix socket. 

Your goal is to correct the configuration, write a service management script, set up port forwarding, and verify the deployment.

Perform the following steps exactly as described:

1. **Backup Strategy**: 
   Before modifying anything, create a backup of the current configuration. Copy `/home/user/appstack/config.json` to `/home/user/backups/config.json.bak`.

2. **Environment Variable & Shell Profile Setup**:
   The backend relies on an environment variable to know where to bind its Unix socket. 
   Add the following line to `/home/user/.bash_profile`:
   `export APP_SOCKET_PATH=/home/user/appstack/run/app.sock`
   Make sure to load this variable into your current session.

3. **Fix the Configuration**:
   Edit `/home/user/appstack/config.json`. The `upstream_socket` key is currently pointing to an incorrect path. Update it so it precisely matches the `APP_SOCKET_PATH` you configured above.

4. **Service Lifecycle Management**:
   The provided `/home/user/appstack/manager.sh` is broken. Completely rewrite it as a robust bash script that accepts `start` and `stop` arguments.
   - When run with `./manager.sh start`, it must:
     a) Start `/home/user/appstack/backend.py` in the background and save its PID to `/home/user/appstack/run/backend.pid`.
     b) Start `/home/user/appstack/proxy.py` in the background and save its PID to `/home/user/appstack/run/proxy.pid`.
   - When run with `./manager.sh stop`, it must read those PID files, terminate the processes gracefully (`kill`), and remove the PID files.
   *(Note: The backend must be started with the `APP_SOCKET_PATH` variable successfully evaluated in its environment).*

5. **Port Forwarding**:
   The proxy service natively listens on `127.0.0.1:8080`. External clients expect to access the service on port `9090`. Since SSH tunneling is restricted in this environment, use `socat` to create a robust port forward running in the background. It must listen on TCP port `9090` and forward traffic to `127.0.0.1:8080`.

6. **Verification**:
   Start your stack using `/home/user/appstack/manager.sh start`. Ensure your `socat` forwarder is running.
   Then, run: `curl -s http://127.0.0.1:9090/status`
   Save the exact, unmodified output of this curl command to `/home/user/final_output.log`.