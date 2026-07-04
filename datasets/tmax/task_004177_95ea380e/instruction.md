You are an AI assistant helping a container specialist manage networking and security for a local microservices environment. We are experiencing an issue where a specific SSH configuration silently rejects key-based logins from certain microservice IPs. Instead of an explicit denial, the connection simply closes right after the public key is offered.

Your task is to create an automated Python-based monitoring and routing remediation system.

1. Write a Python script located at `/home/user/analyze_auth.py`.
2. The script must read a log file at `/home/user/auth.log`. 
   The log file contains entries in this format:
   `[TIME] sshd[PID]: Connection from [IP]`
   `[TIME] sshd[PID]: Offering public key: ...`
   `[TIME] sshd[PID]: Accepted publickey for ...` OR `[TIME] sshd[PID]: Connection closed by [IP]`

3. The script needs to identify "silent rejections". A silent rejection occurs when an IP offers a public key, but the connection is closed WITHOUT a preceding "Accepted publickey" message for that specific PID.
4. For every unique IP address that experiences a silent rejection, the script must append a network routing command to `/home/user/block_routes.sh` to drop traffic from that IP. 
   The exact command to append is: `ip route add blackhole <IP>`
5. Ensure `/home/user/block_routes.sh` is created (if it doesn't exist) and has executable permissions (`chmod +x`).
6. The Python script must implement robust error handling: if `/home/user/auth.log` does not exist, the script must gracefully catch the exception, print "Log not found", and exit with code 0 without creating the shell script.
7. Finally, configure a user cron job to run this Python script exactly every 5 minutes. (e.g., using `crontab`). Specify the absolute path to python3 (e.g., `/usr/bin/python3`) and the script.

To complete the task:
- Create the Python script exactly as specified.
- Set up the cron job.
- Run the Python script once manually so the `/home/user/block_routes.sh` file is generated based on the current `/home/user/auth.log` (assume the log file already exists in the environment).