You are a Linux systems engineer tasked with hardening and deploying a secure internal metrics service. Since you do not have root access (no `sudo`, `iptables`, or `ufw`), you must implement security hardening at the application and file-system levels.

Your objective is to create and configure a multi-component service in the directory `/home/user/service/`. All files must be created by you.

Here are the precise requirements:

**1. Configuration and Secrets Management:**
*   Create `/home/user/service/config.json` containing exactly:
    `{"bind_host": "127.0.0.1", "bind_port": 5050, "log_file": "/home/user/service/access.log"}`
    *Requirement:* This file must have its permissions set to exactly `0600`.
*   Create `/home/user/service/secret.key` containing the exact string: `METRICS_TOKEN_xyz123` (no trailing newline).
    *Requirement:* This file must have its permissions set to exactly `0400`.

**2. The Primary Service (`/home/user/service/server.py`):**
Write a Python 3 script using only standard libraries (e.g., `http.server`, `json`, `os`) that does the following:
*   On startup, it must read the file permissions of `config.json` and `secret.key`. If `config.json` is not exactly `0600` or `secret.key` is not exactly `0400`, the script must immediately print an error and exit with status code `1`.
*   If permissions are correct, it starts an HTTP server binding to the host and port specified in `config.json`.
*   **Endpoints:**
    *   `GET /health`: Returns HTTP 200 with the exact plain text body `OK`.
    *   `GET /metrics`: Reads `secret.key`. If the incoming request has an HTTP header `X-Auth-Token` that exactly matches the contents of `secret.key`, return HTTP 200 with the plain text body `SECURE_METRICS_DATA`. If the header is missing or incorrect, return HTTP 403 Forbidden.

**3. Application-Level Firewall / Port Forwarder (`/home/user/service/firewall_proxy.py`):**
Since we cannot use OS firewalls, you must write a Python 3 TCP proxy that enforces an IP allowlist.
*   The script should listen for incoming TCP connections on `0.0.0.0` port `6060`.
*   When a client connects, the proxy must check the client's IP address.
*   **ACL Rule:** Only allow connections from `127.0.0.1` and `10.0.0.55`.
*   If the IP is allowed, it should forward all bidirectional traffic between the client and the primary service (`127.0.0.1:5050`).
*   If the IP is NOT allowed, it must immediately close the connection without sending any data to the primary service.

**4. Health Check Monitor (`/home/user/service/monitor.sh`):**
Write a bash script that performs a health check on the primary service.
*   It should use `curl` to request `http://127.0.0.1:5050/health`.
*   If the request succeeds and returns `OK`, it must append the exact string `[OK] Service is healthy` followed by a newline to `/home/user/service/monitor.log`.
*   If the request fails or times out, it must append `[ERROR] Service unreachable` followed by a newline to the same log file.
*   Ensure the script is executable (`chmod +x`).

Implement all of the above. Start your background services (the server and the proxy) as part of your final steps to ensure they are running and testable.