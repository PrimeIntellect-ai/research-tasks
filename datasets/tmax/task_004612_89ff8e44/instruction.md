You are investigating a `502 Bad Gateway` error on a locally running user-space Nginx proxy. 

Nginx is configured via `/home/user/nginx/nginx.conf` to listen on `127.0.0.1:8080` and reverse-proxy requests to a local backend via a UNIX domain socket. The backend is a Bash-based HTTP simulator located at `/home/user/app/start_backend.sh`. 

Currently, Nginx returns a 502 error because the backend fails to start correctly due to several configuration, environment, and file-system issues. 

Your task is to fix these issues so that `curl -s http://127.0.0.1:8080` returns a successful HTTP 200 response. Complete the following objectives:

1. **Environment & Profile Setup:** The backend script expects an environment variable `BACKEND_SOCKET` to know where to bind. Add this variable to `/home/user/.bashrc` and set it to `/home/user/app/sockets/backend.sock`.
2. **Directory & Link Management:** The directory `/home/user/app/sockets` is currently broken (it is a dangling symlink). Fix this by creating a real directory at `/home/user/app/sockets` to hold the socket file.
3. **Permissions:** Ensure the `/home/user/app/sockets` directory has exactly `755` permissions, and modify `/home/user/app/start_backend.sh` to ensure any created socket has appropriate permissions (so Nginx can read/write to it). 
4. **Log Rotation:** The Nginx error logs at `/home/user/nginx/logs/error.log` are growing large. Create a simple Bash script at `/home/user/scripts/rotate_logs.sh` that moves `/home/user/nginx/logs/error.log` to `/home/user/nginx/logs/error.log.1` and sends the Nginx master process a `USR1` signal to reopen its log files. Make sure this script is executable.
5. **Validation:** Start or restart Nginx (`nginx -c /home/user/nginx/nginx.conf -p /home/user/nginx/`) and run your fixed `/home/user/app/start_backend.sh` in the background. Once running, execute `curl -s http://127.0.0.1:8080 > /home/user/success.txt`.

Ensure all file paths are exact and that `/home/user/success.txt` contains the actual HTTP response body from the backend.