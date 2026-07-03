You are a cloud architect migrating backend services to a new network topology. To monitor connectivity to the new network ranges during the migration without requiring root access, you need to build a lightweight user-space monitoring script and configure log rotation.

Perform the following tasks:

1. **Automation Script**: Write a Python script at `/home/user/monitor_routes.py`.
   - The script must read a JSON list of IP addresses from `/home/user/targets.json`.
   - For each IP address, it should send exactly one ICMP ping (using the system `ping` command) with a 1-second timeout.
   - It must append the result to `/home/user/migration.log` in the exact format: `<IP> - STATUS: <UP|DOWN>`
   - For example: `127.0.0.1 - STATUS: UP`

2. **Log Configuration**: The logging output will grow quickly once scheduled. Create a logrotate configuration file at `/home/user/logrotate.conf` that targets `/home/user/migration.log` with the following rules:
   - Rotate the log file if its size exceeds 20 bytes.
   - Keep exactly 3 rotated versions.
   - Create a new, empty log file after rotation.
   - Do not compress the rotated logs.

3. **Execution & Rotation Simulation**:
   - Run your Python script `/home/user/monitor_routes.py` once.
   - Run the logrotate utility using your configuration file. Since you are not root, you must specify a custom state file: `logrotate -s /home/user/lr.state /home/user/logrotate.conf`
   - Run your Python script a second time.
   - Run the logrotate utility a second time.

Before you begin, ensure `/home/user/targets.json` exists. If it doesn't, create it with the following exact content:
`["127.0.0.1", "198.51.100.254"]`