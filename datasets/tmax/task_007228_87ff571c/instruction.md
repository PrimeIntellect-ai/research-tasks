You are an edge computing engineer responsible for deploying a custom C-based sensor service to an IoT device. You are operating directly on the device as the user `user` (home directory: `/home/user`). You do not have root access.

Your objective is to fix local connectivity, configure the system data paths, write and compile the sensor service, perform a staged deployment, and set up port forwarding.

Perform the following steps:

1. **Fix SSH Connectivity:** 
   The deployment tooling requires passwordless SSH access to `localhost`. A keypair (`/home/user/.ssh/iot_rsa`) is already authorized, but `ssh -i /home/user/.ssh/iot_rsa user@localhost` is currently failing or prompting for a password due to a misconfiguration in `/home/user/.ssh/config`. Diagnose and fix `/home/user/.ssh/config` so the connection succeeds silently without user interaction.

2. **System Config Management:**
   Create a configuration file at `/home/user/device_fstab.conf`. It must contain exactly one line:
   `DATA_MOUNT=/home/user/sensor_data`

3. **C Service Development:**
   Write a C program at `/home/user/src/edge_server.c`. The program must:
   - Read `/home/user/device_fstab.conf` to extract the directory path defined by `DATA_MOUNT`.
   - Append `/reading.txt` to the extracted path (resulting in `/home/user/sensor_data/reading.txt`).
   - Listen for incoming TCP connections on `127.0.0.1` port `8080`.
   - When a client connects, read the contents of the `reading.txt` file and send the exact contents to the client, then close the connection. (Raw TCP is fine; no HTTP headers are required).
   Compile the program to the executable path `/home/user/src/edge_server`.

4. **Staged Deployment:**
   - Create the directory `/home/user/deploy/v1`.
   - Copy the compiled `edge_server` to `/home/user/deploy/v1/edge_server`.
   - Create a symbolic link at `/home/user/deploy/active` that points to `/home/user/deploy/v1`.
   - Start the `/home/user/deploy/active/edge_server` process in the background.

5. **Port Forwarding:**
   The external diagnostic interface expects to read data on port `9090`. Since the service is bound to port `8080`, set up a persistent SSH local port forward. Run an SSH command in the background that forwards local port `9090` to `127.0.0.1:8080` over a connection to `localhost`, authenticating with `/home/user/.ssh/iot_rsa`.

6. **Verification:**
   Once everything is running, retrieve the sensor reading through the forwarded port by running:
   `nc 127.0.0.1 9090 > /home/user/deploy_result.log`

Ensure all background processes stay running while you perform the final verification step.