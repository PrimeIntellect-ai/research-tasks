You are a deployment engineer preparing a region-aware network update script. 

Your task is to create a Python script and a bash wrapper script that simulate a localized, interactive network configuration rollout.

1. Create a Python script at `/home/user/deploy_update.py` that does the following:
   - Reads the `TZ` and `LC_ALL` environment variables.
   - If `TZ` is exactly `America/New_York` and `LC_ALL` is exactly `fr_CA.UTF-8`, it must prompt the user interactively with the exact string: `Region detected. Confirm deployment? [Y/n]: `
   - If the user enters `Y`, the script must create a file at `/home/user/route_config.cmds` containing exactly these three lines:
     `ip link add name deploy0 type dummy`
     `ip link set deploy0 up`
     `ip route add 10.150.0.0/16 dev deploy0`
   - If the environment variables do not match or the user enters anything other than `Y`, the script should exit with status code 1 without creating the file.

2. Create a bash wrapper script at `/home/user/run_deployment.sh` that:
   - Sets the `TZ` and `LC_ALL` environment variables to the required values.
   - Executes `/home/user/deploy_update.py` and programmatically feeds it the input `Y` to satisfy the interactive prompt.
   - Ensure the bash script is executable (`chmod +x`).

The success of your task will be verified by running `/home/user/run_deployment.sh` and checking the contents of `/home/user/route_config.cmds`. Do not execute the output file as you do not have root privileges to modify the actual system network interfaces.