You are acting as a site administrator managing sandbox environments for user accounts. 

We have a custom, interactive command-line tool for user creation located at `/home/user/bin/usermanager_cli`. It prompts the admin for various details to set up the user, but we need to automate this process for a new batch of users. Also, we need to enforce storage limits via a custom daemon and set up network routing configurations for the user's isolated environment.

Your task is to write and execute a Python script at `/home/user/setup_user.py` that automates this entire user provisioning process. 

The script must perform the following actions:

1. **System Config File Management**: 
   Read the user details from an INI configuration file located at `/home/user/new_user_config.ini`. The file has the following format:
   ```ini
   [NewUser]
   username = <username>
   password = <password>
   network_sandbox = <yes/no>
   quota_mb = <quota_in_megabytes>
   assigned_ip = <ip_address>
   ```

2. **Expect Scripting**: 
   Use the Python `pexpect` module to spawn and interact with the `/home/user/bin/usermanager_cli` tool. You may need to install `pexpect` if it's not already available.
   The tool will prompt you exactly as follows:
   - "Enter username: " (Provide the username from config)
   - "Enter password: " (Provide the password from config)
   - "Enable network sandbox? [y/N]: " (Enter 'y' if network_sandbox is 'yes', otherwise 'N')
   - "Set disk quota (in MB): " (Provide the quota_mb from config)
   
   After the final prompt, the tool will process the input and print a success message in the format:
   `User <username> created with UID <random_uid>.`
   Your script must parse this output to extract the generated integer `UID`.

3. **Network Interface and Routing Configuration**:
   Since actual routing changes require root privileges, your script must generate a bash script at `/home/user/user_routing.sh` that we can run later as root. The script must contain exactly the following line (replace `<assigned_ip>` and `<username>` with the values from the config):
   `ip route add <assigned_ip> dev <username>_veth`
   Ensure the script has executable permissions (0755).

4. **Process Monitoring and Control**:
   We have a custom storage quota enforcer daemon located at `/home/user/bin/quota_daemon.py`. 
   Your script must check if this daemon is currently running. If it is not running, your script must start it in the background (`python3 /home/user/bin/quota_daemon.py`). 
   Capture the Process ID (PID) of the running daemon.

5. **Reporting**:
   Finally, your script must output a JSON file at `/home/user/setup_report.json` containing the gathered information. The JSON must exactly match this structure and data types:
   ```json
   {
     "username": "<username_string>",
     "uid": <uid_integer>,
     "assigned_ip": "<assigned_ip_string>",
     "quota_mb": <quota_mb_integer>,
     "quota_daemon_pid": <daemon_pid_integer>
   }
   ```

After writing the script, execute it so that the user is created, the daemon is running, the routing script is generated, and the JSON report is produced.