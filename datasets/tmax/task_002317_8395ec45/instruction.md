You are an infrastructure engineer tasked with automating the provisioning of a high-throughput load balancer setup to improve the performance of a notoriously slow internal API. 

Currently, our backend service (`/app/backend.py`) takes a fixed 50ms to process any request, capping a single instance at about 20 requests per second. To handle incoming traffic spikes, we need to horizontally scale this service and load balance across multiple instances.

Your task is to write a robust Python provisioning script and configure a reverse proxy to meet our throughput requirements.

Requirements:

1. **Service Provisioning Script**
Create a Python script at `/home/user/provision.py` that performs the following tasks:
- Spawns 4 separate background processes of `python3 /app/backend.py --port <PORT>`, using ports `8001`, `8002`, `8003`, and `8004`.
- Generates a local Nginx configuration file at `/home/user/nginx.conf`. The Nginx server must listen on port `8080` (HTTP) and load balance incoming requests evenly across all 4 backend instances.
- Starts Nginx in the background using the generated configuration (e.g., `nginx -c /home/user/nginx.conf`).
- Implement error handling in your script (e.g., waiting for ports to bind, checking if Nginx started successfully).

2. **Logging and Permissions**
- The Nginx configuration must write access logs to `/home/user/proxy_logs/access.log`.
- Your `provision.py` script must create the `/home/user/proxy_logs` directory and enforce strict ACLs: the directory must have `0700` permissions, and any log files within it must have `0600` permissions.

3. **Log Rotation Setup**
- Write a secondary Python script at `/home/user/rotate.py` that safely rotates the Nginx logs. It should rename `access.log` to `access.log.1`, send the appropriate signal to the Nginx process to reopen its log files, and gracefully handle cases where the log file does not yet exist.

To successfully complete the task:
- You must run your `/home/user/provision.py` script so that the services are actively running and listening.
- A benchmark tool will evaluate your setup by sending 200 concurrent requests to `http://localhost:8080/`. To pass, your load-balanced setup must complete the 200 requests in **under 3.5 seconds**. (A single backend would take >10 seconds).