I am trying to run a local reverse proxy using Nginx as my regular non-root user, but I am receiving a 502 Bad Gateway error when I try to access the service. 

My Nginx configuration is located at `/home/user/nginx.conf` and is configured to listen on port 8888. It expects to proxy requests to an upstream backend via a Unix socket located at `/home/user/backend.sock`. The backend service, however, is missing.

Your task is to implement the missing backend service in Go, set it up to run persistently, and verify the setup:

1. Write a Go HTTP server in `/home/user/main.go` that listens on the Unix socket `/home/user/backend.sock`. 
   - Ensure the server correctly handles the Unix socket creation (hint: you may need to remove the existing socket file before listening if it already exists).
   - The server must respond to `GET /` requests with the exact text: `Backend active` (followed by a newline).
2. Compile the Go program to an executable named `/home/user/backend`.
3. Create a bash wrapper script at `/home/user/start_backend.sh` that starts the `/home/user/backend` executable in the background (make sure the script is executable).
4. Configure a user-level cron job that runs `/home/user/start_backend.sh` every minute (e.g., `* * * * *`). This simulates a basic persistent scheduling mechanism for the service.
5. Execute the start script to start the backend immediately.
6. Start Nginx in the background using the provided configuration: `nginx -c /home/user/nginx.conf`
7. To verify everything is working and the 502 is resolved, make a GET request to `http://127.0.0.1:8888/` and redirect the output to `/home/user/result.log`.

Make sure all created files are located exactly where specified. Do not modify `/home/user/nginx.conf`.