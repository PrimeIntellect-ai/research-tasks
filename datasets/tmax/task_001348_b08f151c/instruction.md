You are a network engineer and DevOps administrator tasked with fixing a broken deployment pipeline for a pair of C-based microservices.

Currently, the deployment fails because the client service cannot reach the server service due to a network configuration mismatch, and the CI/CD pipeline lacks the required pre-flight checks for system storage and user permissions.

Here is your task:

1. **Fix the Connectivity Issue:**
   You have two files located at `/home/user/src/server.c` and `/home/user/src/client.c`. 
   - `server.c` binds to `127.0.0.1` on port `8080` and sends the message "CONNECTION_SUCCESSFUL\n" to any client that connects.
   - `client.c` is currently misconfigured. It attempts to connect to `192.168.1.100` on port `9090`.
   - Modify `/home/user/src/client.c` so that it successfully connects to the server at `127.0.0.1` on port `8080`.

2. **Create a Pre-flight Checker (`/home/user/src/preflight.c`):**
   Write a C program that acts as a deployment pre-flight check. It must perform two system administration validations programmatically:
   - **User Group Administration:** Check if the executing user is a member of the group named `deployers`.
   - **Storage Monitoring:** Use the `statvfs` system call to check if the directory `/home/user/deploy` has at least 1,000,000 bytes (1 MB) of available disk space (`f_bavail * f_frsize`).
   - If both conditions are met, the program must print "PREFLIGHT OK" to `stdout` and exit with status `0`.
   - If either condition fails, it should exit with status `1`.

3. **Construct the CI/CD Pipeline Script (`/home/user/pipeline.sh`):**
   Write a bash script that orchestrates the build, pre-flight checks, and deployment test:
   - Compile `/home/user/src/preflight.c` to `/home/user/preflight`.
   - Run `/home/user/preflight`. If it exits with a non-zero status, the script should exit immediately.
   - Compile `/home/user/src/server.c` to `/home/user/deploy/server` and `/home/user/src/client.c` to `/home/user/deploy/client`.
   - Start the `/home/user/deploy/server` process in the background.
   - Wait for 1 second to ensure the server is ready.
   - Run `/home/user/deploy/client` and redirect its standard output to `/home/user/deploy/result.log`.
   - Terminate the background server process cleanly.

Make sure `/home/user/pipeline.sh` is executable. 

When your pipeline script completes successfully, `/home/user/deploy/result.log` must contain exactly the string "CONNECTION_SUCCESSFUL\n" received from the server.