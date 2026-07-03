You are a Site Reliability Engineer (SRE) tasked with setting up a lightweight, self-healing deployment and monitoring system. You need to combine Git hooks, a basic secure web server, and a custom C-based health checking tool that monitors both the filesystem and the web service.

Your task consists of the following steps:

1. **TLS Configuration**:
   Create a directory `/home/user/tls`. Generate a self-signed RSA (2048-bit) certificate and unencrypted private key, saving them as `/home/user/tls/cert.pem` and `/home/user/tls/key.pem` respectively.

2. **Git Deployment Server**:
   Initialize a bare Git repository at `/home/user/monitor.git`. 
   Create a `post-receive` hook in this repository that does the following:
   - Checks out the pushed code to the working tree directory `/home/user/app` (create this directory).
   - Looks for a file named `server.pid` in `/home/user/app`. If it exists, gracefully kill the process with that PID.
   - Starts the Python web server (which will be pushed in the next step) in the background and writes its new PID to `/home/user/app/server.pid`.

3. **Web Server Code**:
   Clone the bare repository to `/home/user/workspace`. Inside the workspace, write a Python 3 script named `server.py` that starts an HTTPS server on port `8443` binding to `127.0.0.1`. It must use the TLS certificates you generated in Step 1 and serve the current directory. 
   Also, create an empty file named `deploy_success.txt` in the workspace.
   Commit and push these files to the `master` branch of `/home/user/monitor.git`. This should trigger your hook, deploy to `/home/user/app`, and start the server.

4. **C Health Monitor (Filesystem & Network)**:
   Write a C program at `/home/user/checker.c`. This program must:
   - Use `libcurl` to make an HTTPS GET request to `https://127.0.0.1:8443/` (it must disable TLS certificate verification, equivalent to `curl -k`).
   - Use standard C file I/O to check if the file `/home/user/app/deploy_success.txt` exists on the filesystem.
   - If the HTTP response code is 200 AND the file `deploy_success.txt` exists, append the exact string `SYSTEM: OK\n` to `/home/user/system_status.log`.
   - If either check fails, append `SYSTEM: FAIL\n` to `/home/user/system_status.log`.
   
   Compile this C program to `/home/user/checker`. (Ensure you link the curl library using `-lcurl`).

5. **Verification**:
   Execute your compiled `/home/user/checker` program at least once so that `/home/user/system_status.log` is created and contains the initial status. Leave the Python HTTPS server running in the background.