You are a Site Reliability Engineer (SRE) investigating why our local virtualized environment monitor is failing to track VM uptime. The system relies on a QEMU instance and a Python-based monitor communicating over local network ports, but recent misconfigurations have broken the setup. Furthermore, our process supervisor script was accidentally deleted.

Your objective is to restore the service, fix the directory links, and implement a custom Python process supervisor.

Step 1: Fix the Configuration Links
The monitor script expects its configuration file to be located at a specific symlink: `/home/user/service_configs/monitor.json`. Currently, this symlink is broken (pointing to a non-existent legacy path). 
- Update the symlink at `/home/user/service_configs/monitor.json` to point to the correct active configuration file located at `/home/user/system_data/monitor.json`.

Step 2: Recreate the Process Supervisor
Write a Python script at `/home/user/supervisor.py` that acts as a basic process supervisor and restart manager.
- The script must accept a single command-line argument: the path to a JSON file containing a list of command strings.
- Example JSON input: `["echo hello", "sleep 5"]`
- The script must start all commands concurrently as child processes.
- It must monitor the child processes continuously. If any child process exits for any reason, the supervisor must immediately restart it.
- Whenever the supervisor starts a process for the first time, it must append the exact line `STARTED: <command>` to `/home/user/supervisor.log`.
- Whenever it restarts a process that has exited, it must append the exact line `RESTARTED: <command>` to `/home/user/supervisor.log`.

Step 3: Define the Services
Create a JSON file at `/home/user/services.json` containing the following two commands as a JSON array of strings:
1. `"qemu-system-x86_64 -display vnc=127.0.0.1:2 -nodefaults -no-reboot"`
2. `"python3 /home/user/monitor.py"`

Step 4: Run and Verify
Start your supervisor script in the background using the `services.json` file.
The `monitor.py` script will read its configuration via the fixed symlink, connect to the QEMU VNC port (5902), and log the uptime to `/home/user/uptime.log`. 

Leave the supervisor running until `/home/user/uptime.log` contains at least 5 lines of `VNC_OK`. Once this condition is met, your task is complete. (You may forcefully kill a process yourself to test if your supervisor restarts it and logs correctly, but ensure both processes are running at the end).