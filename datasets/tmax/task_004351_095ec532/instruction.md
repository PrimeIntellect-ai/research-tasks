You are a deployment engineer rolling out updates to a fleet of legacy network appliances. Since you do not have direct network access to the physical devices from this environment, you have a local hardware simulator tool at `/home/user/appliance_cli.sh` that reads and writes its state to the local filesystem in `/home/user/appliance_fs/`.

Currently, the simulator is failing. The previous engineer enabled key-based authentication in the appliance's local configuration, but the private key was lost. As a result, the interactive CLI silently rejects all login attempts and immediately terminates.

Your objective is to fix the filesystem-based configuration, write an automation script to interact with the CLI, and deploy the new network interface and routing configuration.

Perform the following steps:

1. **System Config Management:** 
   Inspect and modify the configuration file located at `/home/user/appliance_fs/auth.conf`. You need to change the authentication method so the appliance accepts password-based logins instead of key-based logins. Change `auth_type=key` to `auth_type=password`.

2. **Interactive Script Construction:**
   Create an `expect` script at `/home/user/auto_deploy.exp`. This script must:
   - Execute `/home/user/appliance_cli.sh`.
   - Wait for the `Login: ` prompt and send `admin`.
   - Wait for the `Password: ` prompt and send `admin123`.
   - Wait for the `appliance> ` prompt.

3. **Network Configuration Deployment:**
   Once logged in, your `expect` script must send the following commands to the simulator, waiting for the `appliance> ` prompt after each:
   - `set interface vlan20 192.168.100.1/24`
   - `set route 10.0.0.0/8 192.168.100.254`
   - `commit`
   - `exit`

4. **Execution:**
   Run your script (`expect /home/user/auto_deploy.exp`). The simulator's `commit` command will write the updated routing and interface configurations to `/home/user/appliance_fs/network.conf` and generate a success record in `/home/user/deploy.log`.

Ensure your `expect` script is fully autonomous and handles the interactive prompts correctly. The final state of the system will be verified by checking the contents of `/home/user/appliance_fs/network.conf` and `/home/user/deploy.log`.