You are an edge computing engineer building a local simulation of our IoT device deployment pipeline. You need to write a backend sensor API, configure a load balancer to distribute traffic across multiple instances, and write a deployment script to manage their lifecycle. 

Since you do not have root access, everything must be run in user space using high ports.

Here are your specific instructions:

1. **Create the Edge Application:**
   Write a Python application at `/home/user/edge_app/app.py`.
   - The app must act as a web server listening on a port defined by the `PORT` environment variable.
   - It must read a `SENSOR_ID` environment variable.
   - When a GET request is made to `/health`, it must return a JSON response exactly like: `{"sensor_id": "<SENSOR_ID>", "status": "ok"}` with a 200 OK status code.
   - You may use lightweight frameworks like Flask or FastAPI (you can install them locally via `pip install --user`), or built-in Python libraries.

2. **Configure the Load Balancer:**
   Create an HAProxy configuration file at `/home/user/haproxy.cfg`.
   - It should start a frontend listener on port `9000`.
   - It should load balance (round-robin) across three backend servers on `127.0.0.1` at ports `9001`, `9002`, and `9003`.
   - Ensure it is configured to run entirely in user space (do not change user/group, do not daemonize in a way that requires root, set `pidfile` to `/home/user/haproxy.pid`).

3. **Create the CI/CD Deployment Script:**
   Write a Python script at `/home/user/deploy.py` that orchestrates the container/process lifecycle. When run, it must:
   - Terminate any previously running instances of the app or haproxy managed by this script.
   - Start 3 distinct background processes of `/home/user/edge_app/app.py`:
     - Instance 1: PORT=9001, SENSOR_ID=alpha
     - Instance 2: PORT=9002, SENSOR_ID=beta
     - Instance 3: PORT=9003, SENSOR_ID=gamma
   - Start the HAProxy load balancer in the background using `/home/user/haproxy.cfg`.
   - Wait for all services to be healthy and responsive.
   - Write exactly 4 lines to `/home/user/pids.log` in the following format:
     `alpha:<PID>`
     `beta:<PID>`
     `gamma:<PID>`
     `haproxy:<PID>`

4. **Execution:**
   Run your `deploy.py` script so the services are running in the background. Ensure the load balancer at `http://127.0.0.1:9000/health` successfully routes traffic to all three instances.