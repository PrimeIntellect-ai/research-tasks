You are an infrastructure engineer tasked with fixing a broken automated provisioning setup for a local web service. The system consists of an Nginx reverse proxy routing traffic to a Bash-based backend via a UNIX domain socket. Currently, requests to the Nginx server return a `502 Bad Gateway` error due to a misconfigured upstream socket path, permission issues, and a fragile backend process.

Your objective is to fix the configuration, secure the filesystem permissions, robustify the bash backend, and establish process supervision.

Perform the following tasks:

1. **Fix the Nginx Configuration**: 
   The Nginx configuration is located at `/home/user/nginx/conf/nginx.conf`. It is currently configured to pass requests to `http://unix:/tmp/backend.sock`. However, the backend daemon is configured to create its socket at `/home/user/run/app.sock`. Update the Nginx configuration to point to the correct UNIX socket path.

2. **Filesystem Permissions**:
   Create the directory `/home/user/run/` if it does not exist. The Nginx worker process needs access to the socket file created inside this directory. Set the permissions of the `/home/user/run/` directory to `777` to ensure the socket is fully accessible.

3. **Robustify the Bash Backend**:
   The backend logic is in `/home/user/app.sh`. It is executed for every request by `socat`. Currently, if the `HTTP_USER_AGENT` contains the string `"BadBot"`, the script executes `exit 1`, crashing the process and failing the request. 
   Modify `/home/user/app.sh` so that instead of crashing (`exit 1`), it successfully outputs a valid HTTP `403 Forbidden` response (e.g., `HTTP/1.1 403 Forbidden\r\n\r\nAccess Denied`) and exits cleanly with code `0`.

4. **Process Supervision**:
   The backend listener is started via `/home/user/daemon.sh`. Write a robust supervisor script at `/home/user/supervisor.sh`. This script must:
   - Run `/home/user/daemon.sh` in the foreground.
   - Trap crashes and automatically restart `/home/user/daemon.sh` if it exits.
   - Sleep for 1 second between restarts to prevent tight looping.
   Start your supervisor script in the background.

5. **Start Services**:
   Ensure your backend supervisor is running.
   Start Nginx using the command: `nginx -p /home/user/nginx -c conf/nginx.conf`

6. **Verification Log**:
   To prove the system works, create a script at `/home/user/verify.sh` that makes two `curl` requests to `http://127.0.0.1:8080/`:
   - One standard request.
   - One request with the User-Agent set to `"BadBot"`.
   Save the HTTP status codes of these requests to `/home/user/results.log` (one code per line).

You have successfully completed the task when Nginx is running, the socket is accessible, the backend correctly handles the malicious User-Agent with a 403, and the supervisor ensures high availability of the daemon.