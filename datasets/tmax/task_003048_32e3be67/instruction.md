You are a Linux systems engineer tasked with hardening a local microservice deployment. 

We have a C-based backend application and a local Nginx reverse proxy. Currently, the Nginx configuration is broken (returning a 502 Bad Gateway) because the proxy socket path doesn't match the backend. Furthermore, the backend is currently insecure, opening a Unix socket in `/tmp/` with default permissions.

Your objective is to secure the application, fix the configurations, and build a local CI/CD testing script.

Perform the following tasks:

1. **Backup Strategy**:
   Before making any changes, create a backup of the original configurations. Archive the directories `/home/user/backend` and `/home/user/nginx` into a single compressed tarball located at `/home/user/backup/pre_hardening.tar.gz`.

2. **System Config Hardening**:
   The Nginx configuration file is located at `/home/user/nginx/nginx.conf`. 
   Update the `proxy_pass` directive in this file to point to a secure socket location: `unix:/home/user/backend/secure.sock`. Do not modify other Nginx settings (like PID paths or listening ports).

3. **C Code Modification**:
   The backend source code is located at `/home/user/backend/server.c`. 
   - Modify the source code so that the socket binds to `/home/user/backend/secure.sock` instead of its current `/tmp/` path.
   - Secure the socket by changing its file permissions to `0600` (read/write by owner only) immediately after it is created and bound, using the C standard library `chmod()` function.
   - Compile the modified C code into an executable at `/home/user/backend/server`. You may use `gcc /home/user/backend/server.c -o /home/user/backend/server`.

4. **CI/CD Pipeline Construction**:
   Write a bash script at `/home/user/ci_deploy.sh` that simulates a deployment and testing pipeline. The script must:
   - Ensure the new `/home/user/backend/server` executable is running in the background.
   - Ensure Nginx is started using the command `nginx -c /home/user/nginx/nginx.conf -p /home/user/nginx/`.
   - Wait 1-2 seconds for the services to initialize.
   - Use `curl` to send an HTTP GET request to `http://127.0.0.1:8080/api/status`.
   - Save the exact output of the curl command to `/home/user/pipeline_result.log`.
   - Gracefully stop both the Nginx daemon and the backend C server before the script exits.
   - Ensure the script has executable permissions (`chmod +x`).

Once you have completed all steps, run your `/home/user/ci_deploy.sh` script to generate the final `/home/user/pipeline_result.log`.