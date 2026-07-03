You are a deployment engineer tasked with rolling out "v2" of our internal microservice. Because you are operating in a restricted environment, you must handle the reverse proxying, process monitoring, and deployment entirely in user-space without root access.

Your task consists of creating a complete deployment package in `/home/user/` with the following components:

1. **The C++ Worker Service (`/home/user/src/worker.cpp`)**
Write a C++ program that acts as a simple TCP server. 
- It must accept exactly two command-line arguments: a port number, and an instance ID string (e.g., `./worker 9001 inst_1`).
- It must listen for incoming TCP connections on `127.0.0.1` at the given port.
- For each connection, it should read the incoming message (up to the first newline):
  - If it receives the exact string `VERSION\n`, it should reply with `v2_<instance_id>\n` and close the connection.
  - If it receives the exact string `PING\n`, it should reply with `PONG\n` and close the connection.
  - For any other input, it can simply close the connection.
- Compile this program to `/home/user/bin/worker` (you should create the `bin` directory).

2. **The Reverse Proxy Configuration (`/home/user/nginx/nginx.conf`)**
We need to load-balance traffic to multiple instances of the worker. Create an Nginx configuration file that runs entirely in user-space (do not try to use systemd or root directories).
- It must load balance raw TCP connections using Nginx's `stream` context.
- It should listen on `127.0.0.1:8080`.
- It should proxy connections using a simple round-robin strategy to three backend instances running on `127.0.0.1` at ports `9001`, `9002`, and `9003`.
- Make sure to specify user-writable paths for the `pid` file, `error_log`, and any required temp directories (e.g., `/home/user/nginx/logs/` and `/home/user/nginx/run/`) so Nginx does not fail due to permission errors.

3. **The Process Monitor (`/home/user/monitor.py`)**
Write a Python script that ensures the three worker processes stay alive.
- It should continuously check the health of ports `9001`, `9002`, and `9003` every 2 seconds by sending the `PING\n` command and expecting `PONG\n`.
- If an instance fails to respond, the monitor must automatically spawn a new `/home/user/bin/worker` process on that port with the correct instance ID (`inst_1` for 9001, `inst_2` for 9002, `inst_3` for 9003).

4. **The Deployment Script (`/home/user/deploy.sh`)**
Write an idempotent bash script that orchestrates the entire deployment:
- Creates all necessary directories (`bin`, `src`, `nginx/logs`, `nginx/run`).
- Compiles the C++ source code.
- Gracefully kills any existing `worker`, `monitor.py`, or `nginx` processes owned by the user.
- Starts the three worker instances in the background.
- Starts Nginx using your custom configuration.
- Starts `monitor.py` in the background.

**Execution:**
Once you have created all the files, run your `/home/user/deploy.sh` script. Ensure it exits successfully, the services are running, and Nginx is successfully proxying requests on port 8080.