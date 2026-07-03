As a container specialist managing a custom microservice environment, you need to build a lightweight Python-based orchestrator that acts as a local container manager, and schedule it to run automatically. The orchestrator has a built-in safety mechanism that silently rejects execution if the environment is not configured correctly.

Here are your objectives:

1. **Environment Configuration:**
   Modify your shell profile (`/home/user/.bashrc`) to permanently export the environment variable `DEPLOY_ENV` with the value `production`. 

2. **Develop the Orchestrator (`/home/user/orchestrator.py`):**
   Write a Python script at `/home/user/orchestrator.py` that manages dummy microservices. The script must:
   - Immediately exit with code 0 without doing anything if the environment variable `DEPLOY_ENV` is not strictly equal to `production`.
   - Ensure the directory `/home/user/run/` exists.
   - Scan the directory `/home/user/services/` for any files ending in `.py`.
   - For each `.py` file found, check if it is already running. You can track running services by keeping a PID file at `/home/user/run/services.pid`. The format of this file must be exactly `service_name:PID` on each line (where `service_name` is the filename without the `.py` extension).
   - If a service is not running (or its PID no longer exists), launch it as a background process using `/usr/bin/python3`, and append/update its new PID in `/home/user/run/services.pid`.
   - Make sure `/home/user/orchestrator.py` is executable.

3. **Scheduled Execution:**
   Configure a cron job for the current user to execute `/home/user/orchestrator.py` every 5 minutes. Use the absolute path to both the python executable and the script (e.g., `/usr/bin/python3 /home/user/orchestrator.py`).

Make sure your Python script correctly handles reading and writing the PID file and uses standard libraries (like `os`, `subprocess`, `sys`). The microservices in `/home/user/services/` have already been created for you.