You are a systems engineer tasked with diagnosing and fixing a custom load balancer daemon that is failing to start. The daemon is written in C and runs on a Linux server. Because you do not have root access, everything must be run and configured in your home directory (`/home/user`).

Currently, the startup script for the load balancer fails. You need to investigate the C source code, fix the bugs, configure its environment, automate an interactive upstream configuration tool, and set up a health check.

Here are your specific tasks:

1. **Fix the Load Balancer Daemon:**
   The source code is located at `/home/user/lb_daemon.c`. Currently, it crashes or fails to start for two reasons:
   - It attempts to bind to a privileged port (80) by default. Modify the C code so that it reads the listening port from the `LB_PORT` environment variable. If `LB_PORT` is not set, it should default to `8080`.
   - It causes a segmentation fault because it reads the `UPSTREAM_CONF` environment variable without checking if it is NULL. Modify the code to check if `UPSTREAM_CONF` is set. If it is not set, print an error message to standard error and exit with status code `2`.
   - Compile the fixed code using `gcc` and output the executable to `/home/user/lb_daemon`.

2. **Automate Upstream Configuration:**
   There is an interactive script at `/home/user/init_upstream.sh` that generates the upstream routing configuration. It will sequentially prompt:
   - "Enter upstream port 1: "
   - "Enter upstream port 2: "
   - "Enter upstream port 3: "
   Write an `expect` script at `/home/user/auto_init.exp` that automates running `/home/user/init_upstream.sh` and provides the ports `9001`, `9002`, and `9003` as the answers.
   Run your expect script to generate the configuration file (which the script saves to `/home/user/upstream.conf`).

3. **Configure the Environment:**
   To ensure the daemon runs correctly in the future, append the following environment variable exports to `/home/user/.bash_profile`:
   - `LB_PORT=8080`
   - `UPSTREAM_CONF=/home/user/upstream.conf`

4. **Set Up a Health Check:**
   Write a bash script at `/home/user/health_check.sh` that acts as a monitor. The script must:
   - Use `curl` to make an HTTP GET request to `http://127.0.0.1:8080/health`.
   - If the HTTP status code is 200, it must append the exact string `UP` (followed by a newline) to `/home/user/health.log`.
   - If the request fails or returns any other status code, it must append the exact string `DOWN` (followed by a newline) to `/home/user/health.log`.
   - Ensure `/home/user/health_check.sh` has executable permissions.

Ensure all file paths and names match exactly. Do not start the daemon in the background permanently; just ensure the executable is compiled and the configuration files are ready.