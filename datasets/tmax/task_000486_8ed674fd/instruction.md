You are a site administrator tasked with deploying a secure, resilient microservice that serves user account data. You need to configure the server, ensure proper permissions, and implement a custom process supervisor to keep the service highly available.

The environment has been partially prepared:
- A configuration file simulating a mount table is located at `/home/user/config.fstab`.
- The user account data is located in a directory that is referenced in the fstab file.

Perform the following steps:

1. **Permission Management**
   Find the directory path associated with `accounts_mount` in `/home/user/config.fstab`.
   Change the permissions of this directory to exactly `0700` so only the owner can read/write/execute.

2. **TLS Configuration**
   Create a directory `/home/user/app/`. Inside it, generate a self-signed RSA-2048 certificate and unencrypted private key named `cert.pem` and `key.pem` respectively. Use `/CN=localhost` for the subject.

3. **Web Server Deployment (`/home/user/app/server.py`)**
   Write a Python script that acts as a secure web server.
   - It must dynamically read `/home/user/config.fstab`, find the line starting with `accounts_mount`, and extract the target directory path (the second column).
   - It must start an HTTPS server on `127.0.0.1` port `8443` using Python's built-in `http.server`.
   - It must serve files exclusively from the extracted `accounts_mount` directory.
   - It must use the `cert.pem` and `key.pem` you generated.

4. **Process Supervision (`/home/user/app/supervisor.py`)**
   Write a Python supervisor script to ensure high availability.
   - The script must launch `server.py` as a child process.
   - If the child process exits or crashes for any reason, the supervisor must immediately write the exact string `[RESTART]` to `/home/user/app/supervisor.log` (append mode) and restart `server.py`.
   - The supervisor must run continuously.

5. **Execution**
   Start your supervisor script in the background so that the web server is currently running and supervised when you finish the task. (e.g., `nohup python3 /home/user/app/supervisor.py >/dev/null 2>&1 &`).

Ensure that an automated script can successfully run `curl -k https://127.0.0.1:8443/users.json` to verify the deployment.