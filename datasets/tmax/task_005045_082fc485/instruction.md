You are an edge computing engineer deploying an automated update pipeline for a simulated local IoT device. The device management interface is running locally on port 8888. It requires an interactive login to trigger deployments.

Your task is to set up a Git-based deployment workflow using a Git hook, an Expect script, and some directory management.

Follow these exact steps:

1. Directory and Link Management:
   - Create a bare Git repository at `/home/user/iot_repo.git`.
   - Create a symbolic link at `/home/user/active_repo` that points to `/home/user/iot_repo.git`.
   - Create a deployment directory at `/home/user/deploy_stage`.

2. Task Automation & Network Routing Logging:
   - Create a `post-receive` hook inside the bare repository (`/home/user/iot_repo.git/hooks/post-receive`).
   - The hook must first check out the latest pushed files into `/home/user/deploy_stage`.
   - Next, the hook must execute `ip route get 8.8.8.8` and save the exact standard output to `/home/user/deploy_stage/route_info.txt`.

3. Expect Scripting for Interactive Automation:
   - Create an Expect script at `/home/user/trigger_sync.exp`.
   - The script must connect to the local IoT device simulator via raw TCP (e.g., using `telnet localhost 8888` or `nc localhost 8888`).
   - The simulator will prompt: `Device login:`
   - The script must send the password: `edgeAdmin`
   - The simulator will then prompt: `Command>`
   - The script must send the command: `SYNC /home/user/deploy_stage`
   - The hook (`post-receive`) must execute this Expect script as its final step. Ensure the hook and the Expect script have the correct executable permissions.

4. Trigger the Pipeline:
   - Clone the bare repository to a temporary location (e.g., `/home/user/temp_clone`).
   - Inside the clone, create a file named `firmware.bin` containing exactly the string `v1.2.0`.
   - Commit and push this file to the bare repository to trigger the `post-receive` hook.

If successful, the Git push will automatically deploy the files, log the routing information, and use the Expect script to notify the IoT device. You can check if your deployment worked because the simulated IoT device will write a confirmation log to `/home/user/device_sync_log.txt`.