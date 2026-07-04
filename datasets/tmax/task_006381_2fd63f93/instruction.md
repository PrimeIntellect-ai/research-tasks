You are a capacity planner assisting a systems team with preparing a Python metrics application for production deployment. The deployment uses Nginx as a reverse proxy in front of a Python Gunicorn/Flask application.

Currently, there are a few issues you need to resolve within the user environment (no root access required to complete these tasks). 

Your tasks:
1. **Fix the Nginx 502 Error:** The local user Nginx configuration at `/home/user/nginx/nginx.conf` is currently returning a 502 Bad Gateway when tested. Nginx is trying to route traffic to the Python app via a Unix socket, but the socket path is misconfigured. Inspect the Nginx configuration and the Gunicorn startup script at `/home/user/app/start.sh` to determine the correct socket path. Update `/home/user/nginx/nginx.conf` so the `proxy_pass` points to the correct upstream socket.

2. **Configure Log Rotation:** As a capacity planner, you need Nginx access logs rotated so they don't fill up the disk. Create a standard `logrotate` configuration file at `/home/user/metrics_logrotate.conf` targeting the log file `/home/user/nginx/logs/access.log`. It must specify that logs are rotated `daily`, keep `7` backups, and `compress` them.

3. **Prepare Fstab Entry:** A new storage volume will be attached for capacity metrics. Create a file at `/home/user/capacity_fstab` containing exactly one standard `fstab` line to mount the block device `/dev/nvme1n1` to the directory `/home/user/capacity_metrics`. Use the `xfs` filesystem, `defaults` for options, `0` for dump, and `2` for pass.

4. **Prepare Firewall Rule:** To restrict access to the metrics app, you need an iptables command. Create a bash script at `/home/user/firewall_rule.sh` that contains a single `iptables` command to append a rule (`-A`) to the `INPUT` chain, blocking (`DROP`) TCP traffic (`-p tcp`) from the source IP `192.168.1.100` (`-s`) on destination port `8080` (`--dport`). Ensure the script is executable.

Note: You do not need to restart Nginx or apply the iptables/fstab rules, as an automated root script will do this during deployment. Simply create/modify the required files exactly as specified.