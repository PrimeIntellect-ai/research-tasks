You are a FinOps analyst responsible for optimizing cloud development costs. Developers have been leaving expensive local proxy tunnels running 24/7. To reduce costs, we want to restrict these port-forwarding tunnels to business hours (09:00 to 17:00, inclusive) in the `America/New_York` timezone. 

There is an existing, flawed systemd user unit file at `/home/user/optimizer.service`. Currently, it fails to start reliably because it attempts to run before the local billing tracker is ready.

Your task is to fix the systemd service file and write the Python automation script it calls. 

Step 1: Fix the Systemd Service
Edit `/home/user/optimizer.service` so that:
1. It contains the correct dependency directive to ensure it only starts **after** `billing-api.service`.
2. The `ExecStart` directive must execute `/home/user/cost_optimizer.py` using `python3`.

Step 2: Write the Automation Script
Create a robust Python script at `/home/user/cost_optimizer.py` that does the following:
1. Reads a configuration file located at `/home/user/port_mapping.json`. This file contains a dictionary mapping service names to their ports, e.g., `{"cache": {"listen": 8080, "target": 9090}}`.
2. Determines the current time strictly in the `America/New_York` timezone (regardless of the system's default timezone).
3. Evaluates if the current hour in New York is within business hours (09:00 to 17:00, inclusive of the 17th hour, i.e., up to 17:59).
4. **During business hours:** Generates a bash script at `/home/user/apply_port_rules.sh`. For each service in the JSON config, write a `socat` command to set up local port forwarding in the background. The format must exactly match:
   `socat TCP4-LISTEN:<listen_port>,bind=127.0.0.1,fork TCP4:127.0.0.1:<target_port> &`
5. **Outside business hours:** The generated bash script `/home/user/apply_port_rules.sh` should simply contain the exact line: `echo "Off-hours: tunnels disabled"`
6. **Error Handling:** If `/home/user/port_mapping.json` is missing or invalid JSON, the script must catch the exception and generate the `/home/user/apply_port_rules.sh` file with the exact line: `echo "Error: missing config"`
7. **Permissions:** The Python script must set the file permissions of `/home/user/apply_port_rules.sh` to strictly `700` (read, write, execute only for the owner).

Constraints:
- Use only standard Python 3 libraries (e.g., `json`, `datetime`, `os`, `zoneinfo` or `pytz` if installed).
- Do not attempt to start the systemd service (as you do not have root/dbus access in this environment), just ensure the files are correctly created and configured.