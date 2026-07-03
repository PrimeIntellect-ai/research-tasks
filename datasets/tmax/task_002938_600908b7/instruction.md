You are an SRE tasked with building a custom dynamic load balancer and uptime monitoring system. 

We have a set of unstable microservices running locally on ports 9001, 9002, and 9003. You need to write a C++ daemon that monitors their health, dynamically updates a reverse proxy configuration, and logs their uptime to the filesystem.

Your task is to:
1. Create a local, unprivileged Nginx setup. Write an Nginx configuration file at `/home/user/nginx/nginx.conf` that listens on port `8080` and proxies traffic to an upstream block defined in `/home/user/nginx/upstream.conf`. Configure Nginx to store its PID at `/home/user/nginx/nginx.pid` and its logs inside `/home/user/nginx/logs/` so it doesn't require root access.
2. Write a C++ program at `/home/user/sre_monitor.cpp` that acts as the health checker and service manager. The program must:
   - Loop indefinitely, checking the health of the backends on ports 9001, 9002, and 9003 every 2 seconds by sending an HTTP GET request to `http://127.0.0.1:<port>/health`. (A response of `200 OK` means healthy, anything else or a connection refusal means unhealthy).
   - Write the healthy ports into `/home/user/nginx/upstream.conf` using the Nginx `upstream` syntax (e.g., `server 127.0.0.1:9001;`).
   - If the list of healthy servers changes compared to the previous check, send a `SIGHUP` signal to the Nginx process (read the PID from `/home/user/nginx/nginx.pid`) to reload the configuration.
   - Append the health status of all three ports to a log file at `/home/user/uptime.log` on every check. The exact format must be: `<EPOCH_TIMESTAMP> | 9001:<UP|DOWN> | 9002:<UP|DOWN> | 9003:<UP|DOWN>\n`
3. Compile the C++ program to `/home/user/sre_monitor`. You may use `libcurl` for the HTTP requests.
4. Start Nginx using your custom configuration.
5. Start your `sre_monitor` daemon in the background.

Ensure all directories exist before starting your services. Do not use `sudo` or require root privileges to run Nginx. Leave both Nginx and your compiled `sre_monitor` running in the background when you are finished.