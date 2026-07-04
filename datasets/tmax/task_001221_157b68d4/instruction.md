You are a container specialist managing a custom microservice deployment. One of your legacy microservices runs locally and occasionally stops responding. You need to build a custom health-check diagnostic tool in C++ and schedule it using a robust bash wrapper.

Here are your instructions:

1. **C++ Health Checker:**
   Write a C++ program at `/home/user/health_checker.cpp`. 
   - It must take exactly one command-line argument: the port number.
   - It must establish a TCP connection to `127.0.0.1` on the provided port.
   - Once connected, it must send the string `"PING\n"`.
   - It must then read the response. If the response starts with `"PONG\n"`, the program must exit with status code `0`.
   - If the connection fails, if it times out, or if the response is anything else, the program must exit with status code `1`.
   - Compile this program to `/home/user/health_checker`.

2. **Robust Bash Wrapper:**
   Write a bash script at `/home/user/monitor.sh` that utilizes your new C++ binary to monitor the service running on port `8081`.
   - The script must execute `/home/user/health_checker 8081`.
   - If the checker exits with `0`, the script must append the exact string `UP` (followed by a newline) to `/home/user/health.log`.
   - If the checker exits with `1`, the script must append the exact string `DOWN` (followed by a newline) to `/home/user/health.log`.
   - Make sure `/home/user/monitor.sh` has executable permissions.

3. **Scheduled Task:**
   Install a user-level cron job for the `user` account that executes `/home/user/monitor.sh` every minute. Ensure the cron entry uses the absolute path to the script.

Do not assume the microservice is currently running perfectly, but your tool must be ready to accurately report its status.