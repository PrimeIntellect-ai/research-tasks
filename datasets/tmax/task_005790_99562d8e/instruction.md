You are a Site Reliability Engineer tasked with building a local deployment pipeline and uptime monitoring system. You need to configure a Git-based CI/CD deployment, an HAProxy load balancer, and a custom Python health monitor. 

No root access is available. All services must be run under the local user in `/home/user`.

Here are your requirements:

1. **Git & CI/CD Setup:**
   - Create a bare Git repository at `/home/user/backend.git`.
   - Create a local clone at `/home/user/workspace`.
   - Write a `post-receive` hook in the bare repository (using Python or Bash). When code is pushed to the `main` branch, the hook must:
     - Check out the latest code to two deployment directories: `/home/user/deploy/node1` and `/home/user/deploy/node2`.
     - Terminate any previously running backend servers for these nodes.
     - Start the new backend server in the background for node 1 on port 9001 and node 2 on port 9002.

2. **Application Code:**
   - In your local clone (`/home/user/workspace`), write a Python application `server.py` using only standard libraries (e.g., `http.server` or `wsgiref`).
   - The server must accept a port number as a command-line argument or environment variable.
   - It must handle `GET /health` by returning HTTP 200 with the exact text `OK`.
   - It must handle `GET /` by returning HTTP 200 with the exact text `Node <port>` (e.g., `Node 9001`).
   - Commit and push `server.py` to `backend.git` to trigger your deployment hook.

3. **Reverse Proxy / Load Balancer:**
   - Write an HAProxy configuration file at `/home/user/haproxy.cfg`.
   - It must listen on `127.0.0.1:8080` (frontend).
   - It must load balance requests using a round-robin algorithm across your two backend nodes (`127.0.0.1:9001` and `127.0.0.1:9002`).
   - It must configure health checks for the backends using the `/health` endpoint.
   - Start the HAProxy instance in the background as the local user (e.g., `haproxy -f /home/user/haproxy.cfg -D`).

4. **SRE Health Monitor:**
   - Write a Python monitoring script at `/home/user/monitor.py`.
   - The script must make 10 sequential HTTP GET requests to `http://127.0.0.1:8080/`.
   - It must collect the plain text responses into a Python list.
   - It must save this list as a JSON array to `/home/user/monitor_output.json`.
   - Run the monitor script once so the JSON file is generated.

When you are finished, ensure HAProxy and the two Python backend nodes are running in the background, and the `monitor_output.json` file is correctly populated.