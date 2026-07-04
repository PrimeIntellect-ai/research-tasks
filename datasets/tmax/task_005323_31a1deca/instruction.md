You are a network engineer tasked with recovering and reconfiguring a multi-service application stack that recently experienced a failure. The application consists of a Python API and a Node.js data service, but the startup scripts are currently failing, and external connectivity is broken.

Your goal is to diagnose the services, restore missing data, establish user-space port forwarding, and automate the entire recovery process.

Here are your instructions:

1. **Restore the Configuration and Data:**
   The application resides in `/home/user/app/`. The services are currently failing to start because their configuration and database files are corrupted or missing. 
   You will find a backup archive at `/home/user/backups/app_backup.tar.gz`. Extract this archive. Inside, you will find `config.json` and `data.db`. Place both files directly into `/home/user/app/`.

2. **Diagnose and Configure Services:**
   The `config.json` file dictates the port where the Python API expects the Node.js TCP data service to be running.
   Inspect `/home/user/app/config.json` to find the required TCP port for the data service.
   Modify `/home/user/app/data_service.js` (or set the appropriate environment variable if the script supports it, or edit the file directly) so that the Node.js service listens on the exact port specified in `config.json`.
   Start the services. The Python API runs on `127.0.0.1:5001` (HTTP) and the Node.js service runs on `127.0.0.1:<PORT_FROM_CONFIG>` (TCP).

3. **Establish Port Forwarding:**
   Since you do not have root access to configure `iptables`, use `socat` or another user-space tool to forward external traffic to your local loopback services. 
   - Forward all TCP traffic on `0.0.0.0:8080` to the Python API (HTTP) on `127.0.0.1:5001`.
   - Forward all TCP traffic on `0.0.0.0:8081` directly to the Node.js data service (TCP) on `127.0.0.1:<PORT_FROM_CONFIG>`.

4. **Automate the Workflow:**
   Create a single executable bash script at `/home/user/run_all.sh`. When executed, this script MUST:
   - Extract the backup and place the files in `/home/user/app/`.
   - Start the Node.js data service in the background.
   - Start the Python API service in the background.
   - Establish the `socat` port forwards on `8080` and `8081` in the background.
   Ensure that running `/home/user/run_all.sh` brings up the entire fully functional stack from scratch.

To successfully complete the task, ensure `/home/user/run_all.sh` is running and all external ports (8080, 8081) are actively serving requests.