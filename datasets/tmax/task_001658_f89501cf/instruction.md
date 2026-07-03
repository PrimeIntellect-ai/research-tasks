You are a capacity planner analyzing resource usage for a fleet of lightweight virtual machines. As part of a new reliability initiative, you need to implement a user-space supervision and logging mechanism for a simulated QEMU VM.

Your environment includes a mock QEMU executable located at `/home/user/qemu_mock.py` which simulates a VM process binding to a VNC port.

Your task is to implement the monitoring and log management components:

1. **Supervision Script (`/home/user/capacity_planner.sh`):**
   Write an executable script (in Bash, Python, or your preferred language) that performs a connectivity diagnostic to check if TCP port `5902` is listening on `127.0.0.1` (simulating VNC display `:2`).
   - If the port is **not listening** (connection refused/fails): 
     The script must start the mock VM in the background by executing: `/home/user/qemu_mock.py -vnc :2`
     It must also append the exact string `STATUS: DOWN - ACTION: STARTING VM` to `/home/user/vm_capacity.log`.
   - If the port is **listening** (connection succeeds):
     It must append the exact string `STATUS: UP - ACTION: NONE` to `/home/user/vm_capacity.log`.

2. **Log Rotation Configuration (`/home/user/rotate.conf`):**
   Write a `logrotate` configuration file to manage `/home/user/vm_capacity.log`.
   The configuration must specify:
   - Rotate the log file if its size exceeds `10 bytes`.
   - Keep exactly `2` old rotated copies.
   - Compress the rotated files.
   - Do not throw an error if the log file is missing (`missingok`).

3. **Execution:**
   - Ensure your `/home/user/capacity_planner.sh` is executable.
   - Run your script once (the port will be down, so it should log the DOWN status and start the mock VM).
   - Wait 2 seconds for the mock process to bind to the port.
   - Run your script a second time (the port should now be up, logging the UP status).
   - Manually trigger your logrotate configuration exactly once by running:
     `logrotate -s /home/user/lr.state /home/user/rotate.conf`

Ensure all file paths and log strings exactly match these instructions.