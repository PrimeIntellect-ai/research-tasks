You are a container and deployment specialist managing a set of legacy microservices. Our application architecture uses an Nginx instance configured to load-balance traffic across several local background processes simulating micro-virtual machines.

Currently, the Nginx reverse proxy is returning HTTP 502 Bad Gateway errors. The root cause is a mismatch in the UNIX socket paths: the deployment script is deploying the microservices to hardcoded paths in `/tmp/`, but the active Nginx configuration expects them in `/home/user/run/`.

Your task is to fix the deployment script to implement a proper, automated staged deployment by dynamically reading the correct socket paths from the Nginx configuration.

Here are the requirements:

1. **Target Script**: Modify the existing bash script at `/home/user/deploy_vms.sh`.
2. **Dynamic Configuration Parsing**: The script must read `/home/user/nginx/nginx.conf`, specifically looking for the `server unix:...;` lines inside the `upstream backend` block, to extract the exact socket paths expected by Nginx.
3. **Staged Deployment Implementation**: 
   - Loop through the extracted socket paths in the order they appear in the config.
   - For each socket path, start the microservice emulator by running `/home/user/bin/qemu_mock.sh <socket_path>` in the background.
   - Wait exactly 1 second (`sleep 1`) after starting each process to allow it to initialize before deploying the next one.
4. **Logging**: Immediately after starting each background process (and before the 1-second sleep), append a record to `/home/user/deployment_final.log` in this exact format:
   `DEPLOYED PID <process_id> TO <socket_path>`
   (Replace `<process_id>` with the actual PID of the backgrounded `qemu_mock.sh` command).

Clean up any old running `qemu_mock.sh` processes before running your final script. Make sure you run the modified `/home/user/deploy_vms.sh` script so the processes are active and the log file is generated.