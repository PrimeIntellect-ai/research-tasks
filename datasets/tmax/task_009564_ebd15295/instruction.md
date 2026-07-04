You are acting as a Site Reliability Engineer managing a custom uptime monitoring solution. The monitoring daemon reads its targets from a configuration file located at `/home/user/monitor_config.json`. 

You need to write an idempotent Python script to automate the addition of a new service endpoint to this configuration while ensuring safe backup practices.

Please complete the following tasks:
1. Write a Python script located at `/home/user/update_config.py`.
2. The script must perform the following actions when executed:
   a. Create a backup of `/home/user/monitor_config.json` to `/home/user/monitor_config.json.bak`. If the backup file already exists, do not overwrite it (this preserves the original un-mutated state).
   b. Parse the JSON configuration from `/home/user/monitor_config.json`.
   c. Add a new endpoint to the `endpoints` list with the exact data: `{"name": "cache_service", "url": "http://localhost:8081/health"}`.
   d. Ensure the operation is idempotent. If an endpoint with the name `"cache_service"` already exists in the `endpoints` list, do not add it again.
   e. Write the updated JSON back to `/home/user/monitor_config.json` with an indentation of 4 spaces.
3. Run your Python script so the configuration is updated.

The initial `/home/user/monitor_config.json` file is already on the system. Your script will be tested by inspecting the JSON structure of both the updated config file and the backup file.