As a monitoring specialist, you need to deploy an automated alert system to monitor disk storage for specific users. We have a legacy alerting tool that requires interactive prompts, which you will need to automate.

You are provided with the following environment details:
- A list of user accounts to monitor is located at `/home/user/users_list.txt` (one username per line).
- The data directories for these users are located at `/home/user/data/users/<username>/`.
- A JSON file `/home/user/quotas.json` specifies the maximum allowed disk usage (in bytes) for each user. It has the format: `{"username": quota_in_bytes, ...}`.
- A legacy interactive CLI tool is located at `/home/user/bin/legacy_alerter`. It logs alerts to a central system but requires interactive input.

Your objectives:
1. Write an executable script located at `/home/user/monitor_script`. You may use any language (Bash with `expect`, Python with `pexpect`, etc.).
2. The script must iterate through every user in `/home/user/users_list.txt`.
3. For each user, calculate the total disk usage of their directory in bytes. You MUST use `du -sb /home/user/data/users/<username>` and extract the integer value for the usage.
4. Compare the usage against the user's quota from `/home/user/quotas.json`.
5. If a user's usage strictly exceeds their quota, your script must invoke `/home/user/bin/legacy_alerter` and automate the interaction.
   The tool will prompt exactly as follows (including trailing spaces):
   - `Enter username: ` (You send the username)
   - `Enter current usage (bytes): ` (You send the exact `du -sb` usage integer)
   - `Enter quota (bytes): ` (You send the exact quota integer from the JSON)
   - `Confirm alert (y/n)? ` (You send `y`)
6. Schedule this script to run automatically every 10 minutes using the user's crontab.
7. Finally, run your script once manually so that the alerts are generated immediately.

Ensure your script handles the interactive prompts correctly and finishes executing.