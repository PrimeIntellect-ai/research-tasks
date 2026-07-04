You are an AI assistant helping a cloud architect migrate a legacy service deployment pipeline to a new server environments. You must implement a completely user-space Git-based deployment pipeline, process monitor, and port forwarder using Python and standard Linux tools. You do not have root access.

Please complete the following setup:

1. **Directory Structure & Symlinks:**
   - Create the directory `/home/user/repo/app.git` and initialize it as a bare Git repository.
   - Create directories `/home/user/deployments` and `/home/user/logs`.
   - The active deployment should eventually be symlinked at `/home/user/current_app` pointing to `/home/user/deployments/app`.

2. **Git Deployment Hook:**
   - Write a `post-receive` hook in Python at `/home/user/repo/app.git/hooks/post-receive`. Ensure it is executable.
   - When code is pushed to this repository, the hook must:
     a) Check out the pushed files into `/home/user/deployments/app`.
     b) Update the symlink `/home/user/current_app` to point to `/home/user/deployments/app`.
     c) Terminate any currently running instance of `server.py`.
     d) Start `/home/user/current_app/server.py` in the background.
     e) Redirect the standard output and standard error of `server.py` to `/home/user/logs/app.log`.

3. **Port Forwarding Proxy:**
   - Write a Python script `/home/user/proxy.py` that listens on `127.0.0.1:8080` and forwards all incoming TCP traffic to `127.0.0.1:9090`.
   - Write a shell script `/home/user/start_proxy.sh` that starts `proxy.py` in the background and writes its PID to `/home/user/proxy.pid`. Run this script.

4. **Process Monitoring:**
   - Write a Python script `/home/user/monitor.py` that runs continuously. Every 5 seconds, it should check if `server.py` is running. 
   - If `server.py` is not running (and `/home/user/current_app/server.py` exists), it should start it (appending output to `/home/user/logs/app.log`).
   - Write a shell script `/home/user/start_monitor.sh` that starts `monitor.py` in the background and writes its PID to `/home/user/monitor.pid`. Run this script.

5. **Log Rotation:**
   - Create a logrotate configuration file at `/home/user/logrotate.conf` specifically for `/home/user/logs/app.log`.
   - It must specify: daily rotation, keep 5 backlogs, compress old logs, and use the `copytruncate` option.

Ensure your background processes (`proxy.py` and `monitor.py`) are actually running via your start scripts before completing the task.