You are an infrastructure engineer automating the provisioning of a custom storage monitoring service. The service consists of a C backend listening on a UNIX domain socket and an Nginx reverse proxy serving requests on a local, unprivileged TCP port. 

Currently, our deployment is broken. Nginx returns a 502 Bad Gateway because it is configured with the wrong upstream socket path, and the C backend hasn't been implemented properly to calculate disk usage.

Your objective is to deploy this stack entirely within `/home/user`. Do not use `sudo` or root privileges.

Here are the requirements:

1. **Storage Monitoring Backend (C Language):**
   - Create a C program at `/home/user/src/monitor.c`.
   - The program must act as a simple HTTP server listening on a UNIX domain socket at `/home/user/run/app.sock`.
   - When it accepts a connection, it should calculate the total size (in bytes) of all files inside the `/home/user/data` directory (do not recurse into subdirectories, just the immediate files).
   - It must respond with a valid HTTP response:
     ```
     HTTP/1.1 200 OK\r\n
     Content-Type: text/plain\r\n
     \r\n
     USAGE: <total_size_in_bytes>\n
     ```
   - Close the connection after sending the response.

2. **Nginx Configuration:**
   - Create an Nginx configuration file at `/home/user/nginx/nginx.conf`.
   - It must run as the current user (do not use the `user` directive).
   - Listen on `127.0.0.1:8080`.
   - Proxy all requests to `/status` to the UNIX socket created by your C application.
   - You must store Nginx's PID file at `/home/user/run/nginx.pid` and write logs to `/home/user/nginx/error.log` and `/home/user/nginx/access.log` to avoid permission errors. You will need to configure `client_body_temp_path`, `proxy_temp_path`, `fastcgi_temp_path`, `uwsgi_temp_path`, and `scgi_temp_path` to point to a directory inside `/home/user/nginx/tmp/` to run without root.

3. **Deployment Script:**
   - Write a bash script at `/home/user/deploy.sh` that automates the entire process.
   - The script must:
     - Compile the C program to `/home/user/bin/monitor`.
     - Ensure all required directories (`/home/user/run/`, `/home/user/nginx/tmp/`, etc.) exist.
     - Start the C backend in the background.
     - Start Nginx using the custom configuration file (`nginx -c /home/user/nginx/nginx.conf`).

4. **Verification:**
   - Execute your `deploy.sh` script.
   - Wait 2 seconds for the services to start.
   - Run `curl -s http://127.0.0.1:8080/status > /home/user/result.log`.

Make sure `/home/user/result.log` contains exactly the `USAGE: <bytes>` payload.