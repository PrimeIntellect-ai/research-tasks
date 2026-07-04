You are an infrastructure engineer working on an automated provisioning system. We need a script that acts as a localized storage monitor and dynamically updates a network routing configuration file based on disk usage. Since this runs in a user-space environment without root privileges, the script will generate a configuration file that a separate privileged daemon (which you don't need to build) will apply.

Your objectives:
1. Write a script (in any language you prefer, e.g., Bash or Python) located at `/home/user/storage_router.sh` (or `.py`). Make sure it is executable.
2. The script must calculate the total size (in bytes) of all contents inside the directory `/home/user/data_volume`.
3. Based on the calculated size, it should generate a routing configuration file at `/home/user/routes.conf`:
   - If the total size is strictly greater than 50 Megabytes (52,428,800 bytes), write exactly this line to the file: `10.0.0.0/24 via 192.168.2.254 dev eth1`
   - If the total size is less than or equal to 50 Megabytes, write exactly this line: `10.0.0.0/24 via 192.168.1.1 dev eth0`
4. The script must be idempotent. It should only write to `/home/user/routes.conf` and log an event if the target state is different from the current state (i.e., the content of the file needs to change, or the file doesn't exist yet).
5. When a change is made to the routing configuration, the script must append a log entry to `/home/user/router.log` in this exact format:
   `[YYYY-MM-DD HH:MM:SS] ROUTE_CHANGED: <new_gateway_ip>`
   (e.g., `[2023-10-25 14:30:00] ROUTE_CHANGED: 192.168.1.1`).
6. Schedule this script to run every 5 minutes by adding an entry to the current user's crontab.

Directories:
- `/home/user/data_volume` will already exist, but might be empty. You should test your script to make sure it handles size calculation correctly.

Please implement this and set up the cron job.