You are an observability engineer responsible for managing local dashboard configurations and metric endpoints. You need to write tools to safely back up existing configurations, perform a robust staged deployment of new JSON dashboard rules, and set up local port forwarding for the dashboard UI. 

Your environment does not have root access, so all tools must operate within your home directory (`/home/user`).

Here are your specific tasks:

1. **Staged Deployment & Backup Script**
Write a robust Python script at `/home/user/scripts/deploy_dashboards.py` that performs a staged deployment of dashboard configurations. 
When executed, the script must perform the following actions sequentially:
* **Backup Phase:** Create a gzip-compressed tar archive of the directory `/home/user/dashboards/active/` and save it exactly as `/home/user/backups/dashboard_active_backup.tar.gz`. The archive should contain the files directly (or inside an `active` folder).
* **Validation & Deployment Phase:** Iterate through all `.json` files in `/home/user/dashboards/staging/`.
  * Attempt to parse each file as JSON. 
  * If the file is valid JSON, copy it to `/home/user/dashboards/active/` (overwriting any existing file with the same name).
  * If the file is *invalid* JSON, do NOT copy it. Instead, catch the exception and append exactly this line to `/home/user/logs/deploy_errors.log`: 
    `ERROR: [filename] is invalid JSON.` (Replace `[filename]` with the actual name of the file, e.g., `network.json`).

2. **Dashboard Port Forwarding**
The backend metrics service runs locally on port `9090`, but your observability frontend expects it to be available on port `8080`. 
Write a simple bash script at `/home/user/scripts/forward_dashboard.sh` that uses `socat` to forward TCP port `8080` on all interfaces to TCP port `9090` on `127.0.0.1`. The command should run in the background (using `&` or `fork` correctly). Do not execute this script, just create it.

3. **Execution**
After writing both scripts, execute your `/home/user/scripts/deploy_dashboards.py` script so that the backups are created, the valid JSON files are deployed, and the invalid ones are logged.

Assume the following directories already exist:
- `/home/user/scripts/`
- `/home/user/backups/`
- `/home/user/logs/`
- `/home/user/dashboards/active/`
- `/home/user/dashboards/staging/`

(If they do not exist, you must create them before running your script).