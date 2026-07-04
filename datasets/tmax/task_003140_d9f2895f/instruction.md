You are a deployment engineer rolling out an update for a local network monitoring agent. 

Currently, the deployment is failing for two reasons:
1. The client systemd service starts before the local server service is ready, causing it to crash immediately on boot.
2. The client application, written in C, lacks proper error handling when the server is unavailable.

Your task is to fix these issues and write a robust, idempotent deployment script.

Step 1: Fix the C Application
The source code is located at `/home/user/app/client.c`. It attempts to connect to a server on `127.0.0.1:9090`. 
Update the code so that if the `connect()` call fails, the program does the following:
- Prints exactly `"Error: Connection refused\n"` to standard error (`stderr`).
- Exits with return code `5`.
(Do not change the IP address or port).

Step 2: Fix the Systemd Configuration
The systemd service file template is located at `/home/user/app/netclient.service`.
Modify this file to ensure that `netclient.service` correctly depends on the server. In the `[Unit]` section, add the necessary directives so that `netclient.service`:
- Starts *after* `netserver.service`
- Strictly *requires* `netserver.service` to be active.

Step 3: Create an Idempotent Deployment Script
Write a bash script at `/home/user/app/deploy.sh`. The script must perform the following actions idempotently (meaning it can be run multiple times safely without failing or creating duplicate configurations):
1. Compile `/home/user/app/client.c` into an executable named `/home/user/app/client` using `gcc`. Exit immediately if compilation fails.
2. Ensure the directory `/home/user/.config/systemd/user/` exists.
3. Copy the updated `/home/user/app/netclient.service` to `/home/user/.config/systemd/user/netclient.service` (overwriting any existing file).
4. Write the text `"Deployment script executed successfully"` to a log file at `/home/user/app/deploy.log`.

Make sure to run your script to perform the deployment. We will evaluate the final state of the files and test the compiled `client` executable.