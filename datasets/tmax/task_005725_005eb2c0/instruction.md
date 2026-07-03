You are a FinOps analyst tasked with optimizing our cloud infrastructure costs and fixing a broken local deployment of our metrics service. We use a localized container environment where you must complete several configuration and scripting steps.

Your workspace is `/home/user/finops-scale`. Ensure all created files are in this directory.

Phase 1: Fix the Routing Configuration
Our local Nginx instance (acting as an API gateway) is returning 502 Bad Gateway. The configuration file `/home/user/finops-scale/nginx.conf` has the wrong upstream socket path. It currently points to `/tmp/backend.sock`, but our app actually listens on `/home/user/finops-scale/sockets/app.sock`. 
- Edit `/home/user/finops-scale/nginx.conf` to correct the `proxy_pass` socket path.
- Do not start nginx; just fix the configuration file.

Phase 2: User Account Authorization Configuration
Our cost-management deployment system checks a custom user access file.
- Create a file named `/home/user/finops-scale/finops-users.txt`.
- Add exactly one line for a new user named `cost-saver` belonging to the group `finops-admin`.
- The required format is `username:group:status`, so the line should be exactly: `cost-saver:finops-admin:active`.

Phase 3: Storage Configuration (fstab)
The worker requires a shared data drive to be mapped, but we manage this via a custom fstab mapping file.
- Create a file `/home/user/finops-scale/worker-fstab`.
- Add a single standard fstab entry mapping the image file `/home/user/data-disk.img` to the mount point `/home/user/finops-scale/shared_data`.
- Use the filesystem type `ext4`, options `loop,ro`, dump `0`, and pass `0`. Ensure fields are separated by spaces or tabs.

Phase 4: Cost-Saving Process Monitor Script
We need to dynamically shut down idle workers to save compute costs.
- Write a bash script at `/home/user/finops-scale/scaler.sh`. Make it executable.
- The script should read the last line of `/home/user/finops-scale/metrics.log`.
- If the last line contains the exact string `STATUS:IDLE`, the script must find all running processes with the exact command line name `python3 /home/user/finops-scale/mock-worker.py` and gracefully terminate them (send SIGTERM).
- If the status is `STATUS:BUSY` or anything else, the script should do nothing and exit with status 0.
- (Assume `pgrep` or `pkill` is available, using `-f` for full command line matching is recommended).