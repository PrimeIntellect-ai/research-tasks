You are a network engineer troubleshooting connectivity and latency issues across servers in multiple geographic regions. To test regional routing and analyze failures, you need to process a latency log, build a lightweight timezone-aware backend in C, and configure a local load balancer.

Complete the following objectives:

1. **Text Processing for Latency Analysis:**
   You have a log file located at `/home/user/pings.log`. The file has the format: `[TIMESTAMP] [IP_ADDRESS] [STATUS] latency=[X]ms`
   Using standard Unix text processing tools (like `awk`, `sed`, or `grep`), extract the IP addresses that experienced a latency strictly greater than 150ms. 
   Write these IP addresses to `/home/user/high_latency.txt`. The list must contain unique IP addresses only, with one IP per line.

2. **Timezone-Aware Backend (C):**
   Write a C program at `/home/user/server.c` and compile it to `/home/user/server`.
   - The program must take exactly one command-line argument: the TCP port to listen on.
   - It must listen on `127.0.0.1` at the specified port.
   - For every incoming TCP connection, it must respond with a valid HTTP 200 response. The body of the response must be the current local time formatted exactly as: `YYYY-MM-DD HH:MM:SS TZ` (e.g., `2023-10-25 14:30:00 JST`).
   - The program must respect the `TZ` environment variable to determine its locale/timezone. Use standard C library time functions (e.g., `tzset`, `localtime`, `strftime` with `%Y-%m-%d %H:%M:%S %Z`).
   - Close the connection immediately after sending the response.
   - The program must run persistently (e.g., in a `while(1)` loop) accepting new connections.

3. **Reverse Proxy Configuration:**
   Write an HAProxy configuration file at `/home/user/haproxy.cfg`.
   - Configure a `frontend` that binds to `127.0.0.1:9000` in `http` mode.
   - Configure a `backend` with two servers: `127.0.0.1:9001` and `127.0.0.1:9002`.
   - Use standard `roundrobin` load balancing.

4. **Execution and Logging:**
   - Start an instance of your compiled C server on port `9001` with the environment variable `TZ=Asia/Tokyo` in the background.
   - Start a second instance on port `9002` with the environment variable `TZ=Europe/London` in the background.
   - Start HAProxy in the background using your configuration file (`haproxy -f /home/user/haproxy.cfg`).
   - Wait 2 seconds for the services to initialize.
   - Run `curl -s http://127.0.0.1:9000` exactly 4 times (wait 1 second between each request) and append the raw output of each request to `/home/user/proxy_results.log`. Each output should be on a new line.

Ensure all files are created in `/home/user/` and have the appropriate permissions. Do not use root/sudo.