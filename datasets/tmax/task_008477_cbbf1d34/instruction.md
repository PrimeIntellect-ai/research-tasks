You are a deployment engineer tasked with automating the update of a load balancer configuration based on deployment logs. You do not have root access, so you will build a user-space automation pipeline using Bash.

We have a service deployment process that logs the status of various backend instances to a centralized log file located at `/home/user/deployment.log`. 

Your objective is to write a Bash script that processes this log file to determine which backend ports are currently healthy and successful, and then generates an Nginx `upstream` configuration block for the reverse proxy.

Here is an example of the log format in `/home/user/deployment.log`:
[2023-10-31 14:00:00] [PORT: 8081] [STATUS: IN_PROGRESS]
[2023-10-31 14:01:00] [PORT: 8081] [STATUS: SUCCESS]
[2023-10-31 14:02:00] [PORT: 8082] [STATUS: FAILED]

Perform the following tasks:

1. Create a Bash script at `/home/user/update_lb.sh`.
2. The script must parse `/home/user/deployment.log` (which is in chronological order). A port is considered "healthy" ONLY IF its *most recent* log entry has `[STATUS: SUCCESS]`. If the most recent entry for a port is `FAILED` or `IN_PROGRESS`, it must not be routed to.
3. The script must generate an Nginx configuration file at `/home/user/upstream.conf`. The file must contain exactly this structure, sorting the healthy ports in ascending numerical order:
```nginx
upstream backend_cluster {
    server 127.0.0.1:<PORT_A>;
    server 127.0.0.1:<PORT_B>;
}
```
(Replace `<PORT_A>`, `<PORT_B>`, etc., with the actual healthy ports).
4. Ensure your script `/home/user/update_lb.sh` has executable permissions, and run it once so that `/home/user/upstream.conf` is generated.
5. We need to run this script automatically. Create a cron schedule file at `/home/user/lb.cron` containing a single standard crontab line that schedules `/home/user/update_lb.sh` to run every 5 minutes. (You do not need to install it with `crontab`, just create the text file).

Make sure you follow the formatting of the `upstream.conf` file precisely (including indentation of 4 spaces, and the trailing semicolons).