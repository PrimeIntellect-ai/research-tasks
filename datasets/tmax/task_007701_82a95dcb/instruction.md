You are an infrastructure engineer tasked with stabilizing a data ingestion worker process. Currently, the worker script frequently writes to the wrong location because it relies on environment variables that are missing when started automatically, and there is no monitoring in place to detect when it fails.

Your objective is to wrap this worker in a robust launch script, start it, and create a Python-based health-checking script to monitor its status.

**Environment details:**
- The worker script is located at `/home/user/app/worker.py`.
- The correct data directory for the worker's output is `/home/user/data/`.

**Step 1: Create the Launch Script**
Create a bash script at `/home/user/app/start_worker.sh`. This script must:
1. Export the environment variable `DATA_DIR` set to `/home/user/data`.
2. Execute `/home/user/app/worker.py` in the background.
3. Save the PID of the background process into `/home/user/app/worker.pid`.
4. Ensure the script has executable permissions and execute it to start the worker.

**Step 2: Create the Health Check Script**
Write a Python script at `/home/user/app/health_check.py`. This script must:
1. Read the PID from `/home/user/app/worker.pid`. If the file does not exist or is invalid, treat the process as not running.
2. Verify that the process with this PID is currently running on the system (e.g., by checking `/proc/<pid>`).
3. Verify that the file `/home/user/data/worker.log` exists and has been modified within the last 60 seconds.
4. If both conditions (process is running AND log is fresh) are met, the status is `"healthy"`. Otherwise, the status is `"unhealthy"`.
5. Write the result to `/home/user/app/health.json` in the exact following JSON format:
```json
{
  "status": "healthy",
  "pid": 12345
}
```
*(If the PID cannot be determined, set `"pid": null`)*

**Step 3: Execution**
- Run your `/home/user/app/start_worker.sh` script to launch the worker.
- Wait a few seconds for the worker to write its initial logs.
- Run your `/home/user/app/health_check.py` script so that `/home/user/app/health.json` is generated. 

Make sure all created scripts handle missing files or directories gracefully without crashing.