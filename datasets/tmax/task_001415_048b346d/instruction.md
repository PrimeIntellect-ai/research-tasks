You are a capacity planner analyzing network resource usage to ensure system stability. We need to monitor how many active network connections are being utilized by different user groups on our shared servers, as some groups have been exceeding their connection quotas.

Since you do not have root access to query live system processes comprehensively, the engineering team has exported point-in-time system state files to `/home/user/mock_state/`. 

Your task is to write a Python script `/home/user/net_capacity.py` that acts as a health-check monitor. The script must do the following:

1. Read the network state file `/home/user/mock_state/net_tcp` (formatted exactly like Linux's `/proc/net/tcp`).
2. Read the user account file `/home/user/mock_state/passwd` (standard `/etc/passwd` format) and group file `/home/user/mock_state/group` (standard `/etc/group` format).
3. For every valid connection entry in `net_tcp` (ignoring the header row):
   - Extract the user ID (UID).
   - Find the corresponding username and their primary group ID (GID) from the `passwd` file.
   - Resolve the primary GID to the group name using the `group` file.
   - Tally the total number of network connections per group name.
4. Perform a health check: Determine if any single group has strictly more than 10 connections.
5. Output the results to `/home/user/capacity_report.json` with the exact following structure:
   ```json
   {
       "status": "CRITICAL", // Use "CRITICAL" if any group has > 10 connections, otherwise "OK"
       "group_counts": {
           "developers": 12,
           "analysts": 3,
           "root": 1
       }
   }
   ```
   (Note: Only include groups that have at least 1 connection in `group_counts`).

Run your script to generate the `/home/user/capacity_report.json` file. Ensure your script is robust against standard whitespace-delimited columns in the `net_tcp` file.