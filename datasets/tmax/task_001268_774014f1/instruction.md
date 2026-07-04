You are a deployment engineer verifying a new API release. The development team has provided a new secure web application `/home/user/app/server.py` which runs an HTTPS server on port 8443. It is known to have a bug where a specific endpoint causes it to crash.

Your task is to implement a process supervision script to keep the service highly available and write a Python connectivity and diagnostic script to simulate the rollout and verify the recovery.

Step 1: Process Supervision
Write a bash script at `/home/user/app/supervisor.sh`. 
This script must:
1. Start `/home/user/app/server.py` (use `python3`).
2. Continuously monitor the process. If `server.py` crashes (exits with a non-zero exit code), the supervisor must restart it immediately.
3. Every time it restarts the server, it must append the current UNIX timestamp (seconds since epoch) on a new line to `/home/user/app/restarts.log`.

Step 2: Deployment Diagnostics
Write a Python script at `/home/user/app/deploy_check.py`.
When executed, this script must perform the following actions sequentially:
1. Make an HTTPS GET request to `https://127.0.0.1:8443/health`. Note: The server uses a self-signed certificate, so your script must bypass TLS certificate verification. Record the HTTP status code.
2. Make an HTTPS GET request to `https://127.0.0.1:8443/crash`. This endpoint simulates a fatal error and will cause the server to crash and close the connection. Ignore any connection errors raised here.
3. Sleep for 2 seconds to allow your supervisor script to restart the server.
4. Make another HTTPS GET request to `https://127.0.0.1:8443/health` (bypassing TLS verification again) and record the HTTP status code.
5. Write the recorded status codes to `/home/user/app/diagnostic.json` in the exact following JSON format:
```json
{
  "check1": <HTTP_STATUS_CODE_INT>,
  "check2": <HTTP_STATUS_CODE_INT>
}
```

Constraints:
- Do not modify `/home/user/app/server.py` or the certificate files.
- The supervisor script should run continuously and block the terminal if run directly, but for your testing, you can run it in the background (`./supervisor.sh &`).
- All scripts must be executable.
- Assume Python 3 is installed and `urllib` or `requests` is available.