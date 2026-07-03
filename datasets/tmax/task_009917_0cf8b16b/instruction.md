You are a deployment engineer rolling out updates for an internal application. You need to write an automation script that provisions deployment directories based on a configuration file, but only for valid system users. Finally, you need to configure it as a user-level service.

Perform the following tasks:

1. Write a Python script at `/home/user/rollout.py` that does the following:
   - Reads the configuration file located at `/home/user/targets.conf`. This file contains lines in the format: `directory_name:username`
   - For each line, checks if the `username` is a valid, existing user on the Linux system (e.g., exists in `/etc/passwd`).
   - If the user exists: 
     - Creates a directory at `/home/user/deployments/<directory_name>`. (Assume `/home/user/deployments/` exists).
     - Creates a file named `status.txt` inside that new directory containing exactly the string: `deployed_for_<username>`
   - If the user DOES NOT exist:
     - Appends a line to `/home/user/rollout_errors.log` in exactly this format: `Failed: <directory_name> - <username> not found`
   - Ignore empty lines in `targets.conf`.

2. Make your script executable.

3. Create a user-level systemd service configuration file at `/home/user/.config/systemd/user/rollout.service` to manage this script. 
   - It must include a `[Unit]` section with `Description=Rollout Service`.
   - It must include a `[Service]` section with `Type=oneshot` and `ExecStart=/home/user/rollout.py`.

You do not need to start or enable the systemd service, just create the unit file and the working script, then run the script manually once to generate the outputs.