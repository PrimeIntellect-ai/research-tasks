You are an observability engineer tuning dashboards for a storage node. To feed localized metrics to your observability pipeline, you need to create a custom Python metric gatherer and a bash-based process supervisor.

Since you do not have root access on this node, we will use mock configuration files. 

The simulated environment contains:
- A configuration file at `/home/user/observability/config.ini`
- A mock fstab file at `/home/user/observability/fstab.mock`

Your objective is to write two scripts:

**1. The Exporter Script (`/home/user/exporter.py`)**
Write a Python script that performs the following:
- **System Config & User Check**: Read `/home/user/observability/config.ini`. It has a `[backend]` section with `target_port` and a `[storage]` section with `mount_device`. Check the owner UID of the `config.ini` file. If the script is not running as that UID, exit immediately with code `4`.
- **Mount & fstab**: Parse `/home/user/observability/fstab.mock` to find the exact mount path corresponding to the `mount_device` specified in the config.
- **Connectivity Diagnostics**: Attempt to establish a TCP connection to `127.0.0.1` on the `target_port`. If the connection fails (ConnectionRefused, timeout, etc.), exit with code `2`.
- **Storage Verification**: Check if the mount directory (found in the fstab step) actually exists on the filesystem. If it does not exist, exit with code `3`.
- **Success Metric**: If all checks pass, append a single JSON line to `/home/user/metrics.log` exactly in this format:
  `{"status": "ok", "port": <PORT_INT>, "mount_dir": "<MOUNT_PATH_STRING>"}`
  Then, exit with code `0`.

**2. The Process Supervisor (`/home/user/supervisor.sh`)**
Write a bash script that acts as a custom supervisor for your exporter:
- It must execute `python3 /home/user/exporter.py`.
- If the Python script exits with code `0`, the supervisor should exit cleanly with code `0`.
- If the Python script exits with a non-zero code, the supervisor must append exactly this string to `/home/user/supervisor.log`:
  `Restarting exporter, previous exit code: <CODE>` (replacing `<CODE>` with the actual exit code).
- It should sleep for 1 second, then try again.
- It must restart the exporter a maximum of 3 times (i.e., up to 4 total execution attempts). If it still fails on the final attempt, the supervisor should exit with code `1`.

**Important Constraints:**
- Do not run the scripts yourself; our automated test suite will set up various conditions (creating/deleting the mount directory, opening/closing the port, changing config files) and execute `/home/user/supervisor.sh` to verify your logic.
- Ensure `/home/user/supervisor.sh` is executable (`chmod +x`).
- Do not hardcode the port or mount paths; they must be parsed dynamically.