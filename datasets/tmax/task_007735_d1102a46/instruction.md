You are tasked with building a lightweight, simulated "Kubernetes Operator" written in C that manages application manifests, alongside setting up its environment and networking.

Phase 1: Directory Mapping Configuration (The fstab equivalent)
The operator needs to know where to read manifests and where to write the deployed cluster state. 
Create a configuration file at `/home/user/operator_fstab` with a single line containing two absolute paths separated by a space:
1. The source directory: `/home/user/source_manifests`
2. The destination directory: `/home/user/target_state`

Create both of these directories. Inside `/home/user/source_manifests`, create two files: `deployment.yaml` and `service.yaml`. Write the string "kind: Deployment" in `deployment.yaml` and "kind: Service" in `service.yaml`.

Phase 2: The C Operator Code
Write a C program at `/home/user/operator.c` and compile it to `/home/user/operator`. 
The operator must perform the following actions when executed:
1. Environment/Timezone: Internally set its timezone to `Asia/Tokyo` (using the `TZ` environment variable and `tzset()`).
2. Manifest Processing: Read the `/home/user/operator_fstab` file to dynamically determine the source and destination directories.
3. For every file found in the source directory, read its contents, and write a corresponding file with the exact same name into the destination directory. 
4. Append a newline and the current local time (which will be Tokyo time due to step 1) to the end of the destination file. The appended time strictly follow this format: `[YYYY-MM-DD HH:MM:SS] Applied`.
5. Health Endpoint: Start a TCP listening socket bound to `127.0.0.1` on port `7777`. Whenever a client connects, send the exact string `STATUS: OPERATIONAL` and close the connection. Do this in a loop to keep the program running in the background.

Phase 3: Networking and Tunnels
To securely access the operator's health endpoint, you must set up a local SSH port forwarding tunnel.
1. Ensure you have an SSH key set up locally and authorized in `~/.ssh/authorized_keys` so you can SSH to `localhost` without a password.
2. Establish a background SSH tunnel that forwards local port `8888` to the operator's local port `7777`.
3. Run the compiled `/home/user/operator` in the background so it processes the files and starts listening.
4. Once the tunnel and operator are running, use `nc` or `curl` to fetch the status from port `8888`. Save the exact response to `/home/user/tunnel_test.log`.

Make sure all source code, executables, and log files are placed precisely at the requested paths.