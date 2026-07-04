You are acting as a network engineer troubleshooting a connectivity diagnostic setup. We previously had a cron job running a script that kept dumping network logs into random directories because it relied on relative paths, and sometimes it failed entirely due to broken symlinks.

Your task is to write a robust, idempotent Python script located at `/home/user/run_mtu_check.py` that fixes the directory structure, handles the network diagnostic, and reliably writes the output to the correct location regardless of the current working directory it is executed from.

The script `/home/user/run_mtu_check.py` must perform the following actions when executed:
1. **Directory Management:** Ensure that the directory `/home/user/app_data/network_logs` exists. Create it (and any necessary parent directories) if it does not.
2. **Symlink Management:** Ensure that `/home/user/current_logs` is a symbolic link pointing exactly to `/home/user/app_data/network_logs`. Your script must be idempotent and gracefully handle situations where `/home/user/current_logs` already exists (whether it's a correct symlink, a broken symlink, or a regular file—if it's incorrect, replace it).
3. **Network Diagnostics:** Programmatically retrieve the current network interfaces and their respective MTU (Maximum Transmission Unit) values. You can use system commands like `ip link` via Python's `subprocess` module.
4. **Data Export:** Write a JSON file to `/home/user/current_logs/mtu.json`. The JSON file should contain a single dictionary where the keys are the interface names (strings, e.g., `"lo"`, `"eth0"`) and the values are their corresponding MTU sizes (integers, e.g., `65536`, `1500`). 

Constraints:
- You must write the solution entirely in `/home/user/run_mtu_check.py`.
- Do not assume the script will be run from `/home/user`. It must use absolute paths to resolve locations.
- Ensure the script is fully idempotent (running it multiple times should yield the same correct state without errors).
- Do not use any external third-party libraries (only Python standard library).
- Run your script at least once to ensure the directory, symlink, and `mtu.json` file are successfully created.