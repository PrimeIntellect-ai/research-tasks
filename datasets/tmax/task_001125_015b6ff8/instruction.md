I am an observability engineer tuning our custom dashboards, and I need a reliable way to deploy a lightweight, custom metric exporter written in C. Because we don't have root access on this target environment, we cannot use systemd. Instead, I need you to build a custom service manager, the C-based metric exporter itself, and a CI/CD deployment script that performs a rolling release across multiple instances.

Please complete the following tasks:

1. **The Metric Exporter (C Code):**
   Create a C program at `/home/user/src/metric_exporter.c`.
   - The program should take exactly one command-line argument: the `instance_id` (an integer).
   - It must run in a continuous loop, sleeping for 1 second between iterations.
   - On each iteration, it should overwrite the file `/home/user/metrics_<instance_id>.prom` with the following exact string: `dashboard_metric{instance="<instance_id>"} 100\n`.
   - The program MUST catch the `SIGTERM` signal. When it receives a `SIGTERM`, it should delete its specific `/home/user/metrics_<instance_id>.prom` file and exit gracefully with code 0.

2. **The Service Manager (Bash):**
   Create a SysV-style init script at `/home/user/service_mgr.sh`.
   - It must accept two arguments: `<action>` (start, stop, restart) and `<instance_id>`.
   - `start`: Starts `/home/user/bin/metric_exporter <instance_id>` in the background. It must save the Process ID (PID) to `/home/user/run/metric_exporter_<instance_id>.pid`.
   - `stop`: Reads the PID from the corresponding pidfile, sends a `SIGTERM` to the process, waits for it to exit, and then deletes the pidfile.
   - `restart`: Executes `stop`, then `start`.
   Make sure the script has executable permissions.

3. **The Deployment Pipeline (Bash):**
   Create a deployment script at `/home/user/deploy.sh`.
   When executed, this script must perform a staged rolling deployment:
   - Compile `/home/user/src/metric_exporter.c` using `gcc` into the binary `/home/user/bin/metric_exporter`.
   - Use `/home/user/service_mgr.sh` to `restart` instance `1`.
   - Block/wait until `/home/user/metrics_1.prom` exists and contains the correct payload.
   - Use `/home/user/service_mgr.sh` to `restart` instance `2`.
   - Block/wait until `/home/user/metrics_2.prom` exists.
   - Once both instances have been successfully rolled and verified, write the exact text `ROLLING_DEPLOY_SUCCESS` to `/home/user/deploy.log`.

**Initial Environment Setup:**
Assume you are starting from an empty state. You must create any necessary directories (like `/home/user/src`, `/home/user/bin`, and `/home/user/run`). 

Do not run the deploy script yourself; just create the scripts and the C code. Our automated testing harness will invoke `/home/user/deploy.sh` to verify your solution.