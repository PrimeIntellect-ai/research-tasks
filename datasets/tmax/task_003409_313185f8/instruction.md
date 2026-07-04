You are tasked with diagnosing and fixing a simulated background network service that is failing to start. You do not have root access, so the service is managed by a local user-space supervisor configuration. 

Currently, there is a script located at `/home/user/service/netmon.py` which is supposed to run as a background service and bind to a local port. However, it is failing because it requires a one-time interactive setup to generate its configuration, and its expected directory structure is broken.

Your objectives:
1. **Directory Structure Management:** The script expects a configuration directory at `/home/user/service/conf` and a log directory at `/home/user/service/logs`. Currently, these do not exist or are misplaced. Create `/home/user/real_conf` and `/home/user/real_logs`, and create symbolic links named `conf` and `logs` inside `/home/user/service/` pointing to them respectively.

2. **Interactive Setup via Expect:** The script `netmon.py` must be initialized before it can run as a daemon. Running `python3 /home/user/service/netmon.py --setup` will launch an interactive prompt. You must write an `expect` script at `/home/user/setup_netmon.exp` that automates this setup. The interactive prompts and required answers are:
   - "Enter admin user:" -> Provide `sysadmin`
   - "Enter admin group:" -> Provide `netops`
   - "Enter initialization PIN:" -> Provide `8821`
   Execute your `expect` script to complete the setup. This will generate a configuration file in the `conf` directory.

3. **Process Supervision:** Once initialized, the service should be started. A `supervisord` configuration file is located at `/home/user/supervisor/supervisord.conf`, but the command for the `netmon` program block is currently empty or incorrect. Update the `supervisord.conf` file so that the `command` under `[program:netmon]` runs `python3 /home/user/service/netmon.py --serve`. 

4. **Start the Service:** Start `supervisord` using the configuration file (`supervisord -c /home/user/supervisor/supervisord.conf`). Ensure the `netmon` service enters the RUNNING state.

5. **Verification:** Once the service is successfully running, it will automatically write a status log to `/home/user/service/logs/status.log`. Read this file to ensure it says "SERVICE_ONLINE". 

Create a final file at `/home/user/success.txt` containing the exact text `SERVICE_ONLINE` once you have completed all steps.