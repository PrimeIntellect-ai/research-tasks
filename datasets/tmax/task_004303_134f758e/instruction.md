You are a backup operator tasked with automating the safe restoration of server configuration backups (firewall rules and scheduled tasks) after a recent security incident. Threat actors compromised our backup server and injected malicious cron jobs and backdoor firewall rules into some of our backup archives. 

Your objective involves three main components: extracting legacy management network details, building a Python-based malicious backup detector, and scheduling automated verification.

**Part 1: Recover Legacy Network Details**
We lost the documentation for our legacy management network. However, there is a scanned architectural diagram located at `/app/arch_diagram.png`. Use OCR (e.g., `tesseract`) to read the text in this image. You are looking for a specific string in the format `MANAGEMENT_CIDR: <IP_SUBNET>`. You will need this CIDR block to define what constitutes a "clean" firewall rule.

**Part 2: Build the Backup Sanitizer**
Write a Python script at `/home/user/restore_filter.py`. This script must act as a classifier to determine if a backup configuration file is safe to restore.
The script must accept a directory path as its first positional argument:
`python3 /home/user/restore_filter.py <directory_path>`

It must iterate over all `.conf` files in the given directory and classify each as either "clean" or "evil". It must print a strictly valid JSON object to standard output, where the keys are the basenames of the files (e.g., `backup_1.conf`) and the values are either the string `"clean"` or `"evil"`.

A file is "evil" if it contains:
1. Any `iptables` or `ufw` rule that allows inbound traffic from `0.0.0.0/0` to ports 22, 3306, or 5432.
2. Any cron job definition (lines starting with a cron schedule) that contains the strings `nc -e`, `bash -i`, or `/dev/tcp/`.
3. Any firewall rule allowing access to port 22 where the source CIDR does NOT match the `MANAGEMENT_CIDR` recovered in Part 1.

A file is "clean" if it violates none of these rules.

**Part 3: Schedule the Verification**
Create a cron job file at `/home/user/backup_cron_job`. The file should contain a valid crontab entry that runs the `restore_filter.py` script on the `/home/user/incoming_backups` directory every day at 03:15 AM. The standard output of the cron job must be redirected to `/home/user/backup_scan.log`.

Ensure your script is robust and correctly prints the JSON output to `stdout`. Automated testing will execute your script against hidden evaluation directories to verify your classifier's accuracy.