You are a network engineer troubleshooting a connectivity issue between legacy microservices. Because you lack root privileges to configure `iptables` or system-wide port forwarding, you need to build a user-space Python port forwarder. Additionally, you need to implement strict storage monitoring and log rotation for the forwarding logs to prevent disk exhaustion.

Your task is to implement this connectivity troubleshooting suite by creating the following files exactly as specified.

1. **Environment Setup (`/home/user/network_env.sh`)**
Write a shell script that exports the following environment variables:
- `FWD_LISTEN_PORT=8080`
- `FWD_TARGET_PORT=9090`
- `LOG_DIR=/home/user/logs`

2. **Port Forwarder and Logger (`/home/user/forwarder.py`)**
Write a Python script that acts as a TCP proxy.
- It must read `FWD_LISTEN_PORT` and `FWD_TARGET_PORT` from the environment.
- It must listen on `127.0.0.1` at `FWD_LISTEN_PORT` and forward all incoming TCP traffic to `127.0.0.1` at `FWD_TARGET_PORT`.
- **Log Configuration & Rotation**: It must use Python's built-in `logging` and `logging.handlers.RotatingFileHandler`. Configure it to write to `$LOG_DIR/forwarder.log`. The handler must have `maxBytes=512` and `backupCount=2`.
- Every time a new client connection is accepted, it must log the exact `INFO` level message: `"New connection established"` before forwarding traffic.

3. **Storage Monitoring (`/home/user/check_quota.py`)**
Write a Python script that checks the total disk usage of the directory specified by the `LOG_DIR` environment variable.
- Calculate the total size in bytes of all files in that directory.
- If the total size exceeds 1024 bytes (1 KB), write the exact string `"QUOTA_EXCEEDED"` to a file located at `/home/user/quota_status.txt`.
- If it is 1024 bytes or less, write the exact string `"QUOTA_OK"` to `/home/user/quota_status.txt`.

4. **Integration Script (`/home/user/run_test.sh`)**
Write a bash script to test your setup. It must do the following in order:
- Create the `$LOG_DIR` directory if it doesn't exist.
- Source `/home/user/network_env.sh`.
- Start a dummy destination server in the background: `python3 -m http.server $FWD_TARGET_PORT --bind 127.0.0.1`
- Start `/home/user/forwarder.py` in the background.
- Wait for 2 seconds to ensure services are listening.
- Execute `curl http://127.0.0.1:$FWD_LISTEN_PORT/` and discard the output to `/dev/null`.
- Execute `/home/user/check_quota.py`.
- Gracefully terminate the background `forwarder.py` and `http.server` processes.

Ensure all scripts are executable. The success of this task will be verified by running `/home/user/run_test.sh` and inspecting the logs, output status, and forwarder functionality.