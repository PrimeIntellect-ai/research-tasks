You need to deploy a custom, unprivileged health monitoring service using Python and process supervision. Because you do not have root access, you will use `supervisord` running as the local user, and simulate user management via a JSON registry. 

Your objective is to create an idempotent Bash deployment script (`/home/user/deploy_monitor.sh`) and a Python HTTP server (`/home/user/monitor.py`).

Here are the specific requirements:

**1. The Python Service (`/home/user/monitor.py`):**
* Must use only Python 3 standard libraries (e.g., `http.server`, `json`, `os`).
* Must listen on `127.0.0.1` port `8443`.
* Must implement two GET endpoints:
  * `/health`: Returns HTTP 200 with a JSON payload containing the environment variables `TZ` and `LANG`. Format exactly as: `{"status": "ok", "timezone": "<value_of_TZ>", "locale": "<value_of_LANG>"}`.
  * `/users`: Reads and returns the raw JSON contents of `/home/user/config/users.json`. If the file doesn't exist, return HTTP 404.

**2. The Deployment Script (`/home/user/deploy_monitor.sh`):**
* Must be completely **idempotent** (safe to run multiple times without causing errors, port conflicts, or duplicating running processes).
* Create the directory `/home/user/config/` if it does not exist.
* Generate a local user registry at `/home/user/config/users.json` with exactly this content:
  `{"groups": {"admin": ["alice"], "monitors": ["bob", "charlie"]}}`
* Create a Supervisord configuration file at `/home/user/supervisord.conf`.
  * It must define a program named `health_monitor` that runs `python3 /home/user/monitor.py`.
  * It must enforce a restart policy (autorestart=true).
  * It must set the environment variables for the program to: `TZ="America/St_Johns"` and `LANG="fr_CA.UTF-8"`.
  * Include basic supervisord boilerplate so it can run unprivileged (pidfile in `/home/user/supervisord.pid`, logfile in `/home/user/supervisord.log`, etc.).
* Start `supervisord` using this configuration if it is not already running. If it is running, instruct it to update/reload the configuration without breaking idempotency.
* Wait for the service to be available, then execute a `curl` request to `http://127.0.0.1:8443/health` and save the exact HTTP response body to `/home/user/health_result.log`.

Make sure `/home/user/deploy_monitor.sh` is executable and execute it to finalize the setup. Leave the service running in the background via supervisord.