You are a deployment engineer tasked with rolling out a new routing configuration to a legacy edge router. The router runs inside a virtualized environment, and its management console is exposed via a local TCP serial bridge on `localhost:5000`. It does not support standard APIs, so you must use interactive expect-based automation to push the update.

Your objective is to write a Python script that automates the deployment of the new configuration, and then update the local deployment directory structure to reflect the rollout.

Here are the requirements:

1. **Deployment Directory Structure:**
   In `/home/user/deployments/`, there are two configuration files: `v1.conf` and `v2.conf`. There is also a symbolic link `/home/user/deployments/active` currently pointing to `v1.conf`.

2. **Interactive Automation:**
   Write a Python script at `/home/user/deploy.py` using the `pexpect` library. The script must do the following:
   - Connect to the router's serial console by spawning a `telnet localhost 5000` session.
   - Wait for the `Username: ` prompt and send the username: `admin`.
   - Wait for the `Password: ` prompt and send the password: `enable_secret`.
   - Wait for the main prompt, which is exactly `edge-router# `.
   - Read the contents of `/home/user/deployments/v2.conf`.
   - Send the command `configure terminal`.
   - Wait for the `edge-router(config)# ` prompt.
   - For each line in `v2.conf`, send the line to the console and wait for the `edge-router(config)# ` prompt to return.
   - Send the command `commit`.
   - Wait for the message `Commit successful.`
   - Send the command `exit` to return to the main prompt, then `logout` to disconnect.

3. **Symlink Update:**
   After the script successfully pushes the configuration to the router, update the symbolic link at `/home/user/deployments/active` to point to `/home/user/deployments/v2.conf`. 

Execute your Python script to perform the deployment and ensure the symlink is updated correctly. The simulated router will save its committed configuration to `/home/user/router_state.json` once the `commit` command is successfully executed.