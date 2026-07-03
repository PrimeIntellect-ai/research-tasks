You are a monitoring specialist tasked with setting up a custom health-check daemon and its deployment pipeline. We have a microservice that runs locally, but it sometimes crashes. Since we don't have access to standard monitoring tools in this restricted environment, you need to write a custom C program to monitor it and a deployment script to act as a lightweight CI/CD pipeline.

Please complete the following steps:

1. Write a C program at `/home/user/net_monitor.c`:
   - It must read the environment variable `TARGET_PORT` to know which TCP port to monitor on `127.0.0.1`.
   - It should continuously attempt to open a TCP connection to this port every 1 second.
   - If the connection fails for 3 consecutive attempts, the program must append the exact string `[CRITICAL] Port <PORT> unresponsive. Executing container restart.\n` (where `<PORT>` is the value of `TARGET_PORT`) to the file `/home/user/monitor_alerts.log`.
   - After writing the alert, it must flush the log file and cleanly exit with code 0.
   - If a connection succeeds, the consecutive failure counter should reset to 0. Be sure to close the socket after each successful check.

2. Create a deployment pipeline script at `/home/user/deploy.sh` that does the following:
   - Modifies the shell profile `/home/user/.bashrc` to append the environment variable `export MONITOR_DEPLOYED=true`.
   - Compiles the `/home/user/net_monitor.c` program using `gcc`, outputting the executable to `/home/user/net_monitor`.
   - Sets the environment variable `TARGET_PORT=8080`.
   - Starts the compiled `/home/user/net_monitor` binary in the background.
   - Saves the Process ID (PID) of the background monitor process into a file at `/home/user/monitor.pid`.
   - The script must be executable.

Ensure your C code handles socket creation, connection, and cleanup properly. You may use a standard language like Python (e.g., `python3 -m http.server 8080`) to temporarily spin up a service and test your code before finishing. 

Make sure the file permissions for `deploy.sh` allow execution, and that all files are created exactly at the specified paths.