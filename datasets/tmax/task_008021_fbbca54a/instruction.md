You are an edge computing engineer responsible for deploying code to remote IoT devices. Since direct deployment is often restricted by NATs and firewalls, you must build a lightweight, Git-based CI/CD pipeline that triggers over an SSH tunnel.

Your task is to create an automated deployment setup entirely using Bash. You must write a script at `/home/user/setup_edge_pipeline.sh` that, when executed, performs the following exact steps:

1. **Git Server & CI/CD Hook Configuration:**
   - Create a bare Git repository at `/home/user/iot-device.git` to act as the central deployment server.
   - Configure a `post-receive` hook in this bare repository.
   - The hook must automatically extract the pushed code into a deployment directory at `/home/user/iot-active`.
   - After extraction, the hook must write the exact string `DEPLOYMENT_SUCCESSFUL` followed by a newline to a log file at `/home/user/deploy.log`.

2. **Local Workspace Setup:**
   - Create a local Git repository at `/home/user/workspace`.
   - Create a file named `sensor_app.sh` inside `/home/user/workspace` containing the text: `echo "Reading sensor data"`
   - Commit this file to the `master` branch.
   - Add the bare repository (`/home/user/iot-device.git`) as a remote named `edge`.

3. **Tunneling and Triggering (The Pipeline):**
   - The script must establish a background SSH tunnel that forwards local port `9999` to `localhost:8888`. (Assume passwordless SSH to `user@localhost` is already configured). 
   - Wait 2 seconds for the tunnel to establish.
   - Push the `master` branch of the `/home/user/workspace` repository to the `edge` remote.
   - Finally, the script must gracefully terminate the background SSH tunnel process it started.

Ensure your script is executable (`chmod +x /home/user/setup_edge_pipeline.sh`). Make sure directories are created as needed and that the `post-receive` hook has the correct permissions to execute. Do not execute the script yourself; the automated testing suite will execute `/home/user/setup_edge_pipeline.sh` to verify your solution.