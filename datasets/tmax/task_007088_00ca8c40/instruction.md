You are a system administrator maintaining a local application storage router. We have several storage nodes in the `/home/user/app_data/` directory. Traffic is routed to these nodes based on a network configuration file located at `/home/user/config/router.json`.

Recently, we've had issues with storage nodes running out of disk space. I need you to create a multi-language automated solution to monitor these disk quotas and idempotently update the routing configuration.

Here are the requirements:
1. Write a Python script located at `/home/user/scripts/update_routing.py`. This script should:
   - Calculate the disk usage of each node directory specified in `/home/user/config/router.json` (look under the `"nodes"` key).
   - A node should be marked `"offline"` in the config if its disk usage exceeds 40 Megabytes (40960 Kilobytes). Otherwise, it should be `"online"`.
   - Update the `/home/user/config/router.json` file in-place. The modification must be **idempotent** (running it multiple times should yield the same valid JSON without duplicating entries) and must preserve any other existing keys in the JSON (like `"global_settings"`).

2. Write a Bash wrapper script at `/home/user/scripts/run_checks.sh` that executes your Python script. 
   - After executing the Python script, the Bash script must copy the updated configuration file to `/home/user/logs/final_router.json`.

Make sure you create the `/home/user/scripts` and `/home/user/logs` directories if they do not exist. 
Run your wrapper script to perform the update.

Ensure that your solution correctly parses the paths out of the JSON and updates the `"status"` fields accordingly. Do not hardcode the node names in your script, as they might change.