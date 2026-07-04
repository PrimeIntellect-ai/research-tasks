Hello! I need you to set up a local load balancer with TLS termination using Nginx, but it must run entirely without root privileges. Here are the specific requirements:

1. **Environment Variables**: Add environment variables `BACKEND_A=9001` and `BACKEND_B=9002` to `/home/user/.bashrc`.

2. **TLS Certificate**: Generate a self-signed RSA 2048-bit certificate and key at `/home/user/ssl/server.crt` and `/home/user/ssl/server.key`. The Common Name (CN) must be `localhost`. Make sure to create the directory first.

3. **Backend Servers**: Create a Bash script at `/home/user/backends.sh` that starts two separate web servers in the background. 
   - The servers must listen on the ports defined by `BACKEND_A` and `BACKEND_B` (the script should read these from the environment or `.bashrc`).
   - The server on `BACKEND_A` must serve a response containing exactly the text `Backend A` for any HTTP GET request to its root.
   - The server on `BACKEND_B` must serve exactly the text `Backend B`.
   - You can use Python's `http.server` (creating separate directories with `index.html` files) or any other unprivileged method.
   - Make the script executable.

4. **Nginx Configuration**: Create an Nginx configuration file at `/home/user/nginx/conf/nginx.conf`. It must:
   - Run without root privileges. Omit any `user` directive.
   - Use `/home/user/nginx/nginx.pid` for the PID file.
   - Use `/home/user/nginx/logs/error.log` for the error log.
   - In the `http` block, configure `access_log` to `/home/user/nginx/logs/access.log`.
   - To avoid permission errors, set `client_body_temp_path`, `proxy_temp_path`, `fastcgi_temp_path`, `uwsgi_temp_path`, and `scgi_temp_path` to point to respective subdirectories inside `/home/user/nginx/tmp/`.
   - Listen on port `8443` with SSL enabled, using the certificate and key you generated in step 2.
   - Act as a reverse proxy and round-robin load balancer forwarding requests to `127.0.0.1:9001` and `127.0.0.1:9002`.

5. **Start Script**: Create an executable Bash script at `/home/user/start_all.sh` that:
   - Creates any necessary Nginx directories (like `logs`, `tmp`, etc.).
   - Sources `.bashrc`.
   - Runs `/home/user/backends.sh`.
   - Starts Nginx using your configuration: `nginx -p /home/user/nginx -c conf/nginx.conf`.

Please ensure all scripts are executable and the configuration is valid.