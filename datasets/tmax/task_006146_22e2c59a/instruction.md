You are a network engineer troubleshooting an intermittent uplink issue. To track the connection state and alert the team automatically, you need to set up a monitoring workflow using `expect`, Git hooks, and a simulated email alert system.

A mock network appliance script is located at `/home/user/appliance.py`. It simulates a router console.

Your task is to build the automation pipeline:

1. **Expect Script**: Write an Expect script at `/home/user/check_link.exp` that executes `/home/user/appliance.py`. 
   - It must wait for the prompt `Username: ` and send `admin`.
   - It must wait for `Password: ` and send `netadmin99`.
   - It must wait for the router prompt `router# ` and send the command `check-uplink`.
   - The appliance will respond with either `Uplink is UP` or `Uplink is DOWN`, followed by the `router# ` prompt.
   - It must then send `exit` to close the session.

2. **Git Repository**: Initialize a Git repository at `/home/user/net-logs`.

3. **Wrapper Script**: Write a Bash script at `/home/user/monitor.sh`. This script should:
   - Run the `/home/user/check_link.exp` script and capture its output.
   - Parse the output to determine if the link is "UP" or "DOWN".
   - Write the exact string `UP` or `DOWN` into `/home/user/net-logs/status.txt`.
   - Change directory to `/home/user/net-logs`, add `status.txt` to Git, and commit the change.
   - The commit message must be exactly `Status: UP` or `Status: DOWN` corresponding to the result.

4. **Git Hook & Email Alert**: Create a `post-commit` hook in the Git repository (`/home/user/net-logs/.git/hooks/post-commit`) written in Python.
   - The hook must inspect the latest commit message.
   - If the commit message is `Status: DOWN`, the hook must send an email via SMTP to `localhost` on port `8025`.
   - The email envelope sender (from) must be `monitor@local.net`.
   - The email envelope recipient (to) must be `net-admins@local.net`.
   - The email subject must be `ALERT: Link is DOWN`.
   - If the commit message is `Status: UP`, it should do nothing and exit cleanly.

Ensure all scripts (`check_link.exp`, `monitor.sh`, and the Git hook) are executable.