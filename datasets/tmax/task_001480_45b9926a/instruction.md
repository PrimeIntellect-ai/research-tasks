You are a monitoring specialist tasked with setting up an automated log processing and alerting mechanism for our network sensors. Due to permission constraints, you will be working entirely within your home directory `/home/user`. 

Our network sensors periodically write connection logs to a centralized directory, but the underlying storage must be prepared properly, and we need a script to parse these logs, generate alerts, and perform basic log rotation.

Please perform the following tasks:

1. **Directory Structure and Linking:**
   - Create a directory for the actual log storage at `/home/user/storage/net_logs`.
   - Create a symlink at `/home/user/logs` that points to `/home/user/storage/net_logs`.
   - Create a directory for mail alerts at `/home/user/mail`.

2. **Mock fstab Configuration:**
   - We plan to mount a remote share to this storage directory later. Create a file named `/home/user/my_fstab`.
   - Add exactly the following line to `/home/user/my_fstab` to document the future mount point:
     `//10.0.0.50/netdata /home/user/storage/net_logs cifs defaults,ro 0 0`

3. **Automation Script (`/home/user/net_alert.sh`):**
   - Write a bash script at `/home/user/net_alert.sh` that takes a single argument: the path to a log file (e.g., `/home/user/logs/sensor.log`).
   - The script must read the provided log file. The log lines will follow this format:
     `TIMESTAMP IP=<IP_ADDRESS> STATE=<UP|DOWN> PING=<MS>`
   - For every line where `STATE=DOWN`, the script must append an alert message to `/home/user/mail/alerts.txt`. The alert message must be exactly: `ALERT: Host <IP_ADDRESS> is DOWN` (replace `<IP_ADDRESS>` with the actual IP extracted from the log line).
   - After parsing the log file, the script must perform a basic rotation: move the processed log file to `<original_file_path>.bak` (overwriting any previous `.bak` file) and create a new, empty file at the original log file path.
   - Make sure `/home/user/net_alert.sh` is executable.

Ensure your script works cleanly using standard Bash built-ins and coreutils like `grep`, `awk`, or `sed`. Do not start any long-running daemons. The verification system will test your script by placing a dummy log file in the directory and executing your script.