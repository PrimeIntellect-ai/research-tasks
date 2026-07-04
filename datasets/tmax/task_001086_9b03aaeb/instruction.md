You are an edge computing engineer responsible for deploying configuration updates to a fleet of IoT devices. 

Our hardware vendor provided a proprietary configuration utility located at `/home/user/iot_setup_cli`. Unfortunately, this utility is strictly interactive—it prompts the user for inputs one by one and does not accept command-line arguments. 

You need to automate this deployment process for a batch of new edge devices. 

Here are the details:
1. You have an inventory file at `/home/user/device_inventory.csv` containing the configuration data. The file has no header and uses the format: `Device_ID,Auth_Token,Region,Enable_Telemetry` (e.g., `edge-001,secret123,US,y`).
2. The interactive utility `/home/user/iot_setup_cli` asks exactly the following prompts in order:
   - `Device ID: `
   - `Authentication Token: `
   - `Target Region (US/EU/AP): `
   - `Enable telemetry stream? (y/n): `
   - `Commit configuration? (yes/no): ` (You must answer `yes` to save).

Your task:
Write a Python script at `/home/user/deploy_fleet.py` that reads `/home/user/device_inventory.csv` and automates the interactive utility for every device in the list. You should use the `pexpect` library in Python to handle the interactive prompts. 

When your script runs, it should successfully drive the `/home/user/iot_setup_cli` executable for all devices in the CSV. The CLI tool will automatically generate configuration files in `/home/user/device_configs/` if the interactive sequence is completed successfully. Run your script to generate these configuration files.

Constraints:
- Do not modify the `/home/user/iot_setup_cli` executable.
- Your script must be written in Python 3.
- Ensure all generated configuration files are present in `/home/user/device_configs/` when you are finished.