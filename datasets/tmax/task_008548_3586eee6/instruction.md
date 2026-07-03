You are a Linux systems engineer tasked with hardening and deploying a user-space network configuration without root access. 

An internal application is expected to run on `127.0.0.1:9090`, but for security and architectural reasons, clients must only connect to `127.0.0.1:8080`. Your objective is to deploy a resilient, timezone-aware port forwarding mechanism using Python and user-level scheduling.

Please complete the following steps:

1. **Locale/Timezone Configuration:**
   Configure the user's default timezone to `Asia/Tokyo` by adding the appropriate `TZ` environment variable export to `/home/user/.bashrc`.

2. **User-Space Port Forwarder:**
   Write a Python script at `/home/user/port_forward.py` that binds to `127.0.0.1:8080`. It must accept incoming TCP connections and seamlessly forward all data bidirectionally to `127.0.0.1:9090`. The script must run continuously until terminated.

3. **Process Monitoring:**
   Write a Python script at `/home/user/monitor.py` that checks if `port_forward.py` is currently running in the process list. If it is not running, the script must start it in the background (e.g., using `subprocess.Popen` or standard shell detachment).

4. **Scheduled Task:**
   Install a user crontab that executes `/usr/bin/python3 /home/user/monitor.py` every single minute to ensure the port forwarder is highly available.

Ensure all scripts have the correct paths and are executable if necessary. Do not rely on root/sudo privileges.