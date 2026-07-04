You are a backup operator tasked with testing the restoration of network configurations to a simulated core router. 

We have a proprietary router simulator located at `/home/user/mock_router.py`. This simulator uses an interactive, text-based shell interface (similar to typical network appliances). 

Your goal is to write a Python script using the `pexpect` library to automate the process of reading a backup configuration file, interacting with the simulated router, applying the restored configurations (users, network interfaces, and routes), and then dumping the final verified state to a file.

Here are the specifics:

1. **The Backup File**: You will find the backup configuration at `/home/user/backup_data.json`. It contains a JSON object with keys `users`, `interfaces`, and `routes`.

2. **The Router Simulator (`/home/user/mock_router.py`)**:
   - When executed (`python3 /home/user/mock_router.py`), it presents a prompt: `Router> `
   - You must first log in using the command: `login admin admin` (Returns `Login successful.` or `Error...`)
   - It supports the following configuration commands:
     - `user add <username> <group>` (e.g., `user add jdoe operators`)
     - `interface set <iface_name> <ip_with_cidr>` (e.g., `interface set eth0 192.168.1.10/24`)
     - `route add <destination_cidr> <gateway_ip>` (e.g., `route add 0.0.0.0/0 192.168.1.1`)
     - `dump` (Prints the current system state in JSON format to the console)
     - `exit` (Saves state and exits the simulator)
   - Every successful command returns a confirmation starting with `OK: `.

3. **Your Script**: 
   - Write a Python script at `/home/user/restore_tool.py`.
   - The script must read `/home/user/backup_data.json`.
   - Use `pexpect` to spawn `python3 /home/user/mock_router.py`.
   - Log in, then iterate through the users, interfaces, and routes in the backup file and issue the corresponding commands to the simulator.
   - After applying all configurations, issue the `dump` command.
   - Capture the JSON output from the `dump` command and save it EXACTLY as it is to `/home/user/final_state.json`.
   - Finally, cleanly `exit` the simulator.

Ensure you install any missing Python dependencies like `pexpect` (e.g., `pip install pexpect`) locally if needed.

The final evaluation will check the contents of `/home/user/final_state.json` to ensure the backup was correctly and completely restored.