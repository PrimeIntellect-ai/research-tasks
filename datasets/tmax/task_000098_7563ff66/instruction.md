We are hardening a Linux system against abuse. A previous systems engineer left a configuration spec as an image at `/app/config_spec.png`. We currently have a malfunctioning Nginx configuration at `/home/user/nginx.conf` that returns a 502 Bad Gateway because the upstream socket path is incorrect.

Your tasks are as follows:

1. Extract details from the image:
Use OCR (e.g., `tesseract`) to read the text in `/app/config_spec.png`. You will find two critical pieces of information:
- The correct backend socket path (format: `unix:/path/to/sock`).
- The rate limit threshold (maximum allowed requests per second).

2. Fix the Nginx configuration:
Create a fixed version of the Nginx configuration at `/home/user/nginx_fixed.conf` by replacing the incorrect upstream socket path in `/home/user/nginx.conf` with the one extracted from the image.

3. Log analysis and firewall automation:
An Nginx access log is located at `/app/access.log`. We need to block IPs that have exceeded the rate limit threshold specified in the image.
Write a Bash script at `/home/user/harden.sh` that:
- Reads the path to the log file from the `LOG_PATH` environment variable.
- Parses the log to identify any IP address that made strictly more requests than the rate limit threshold within any single calendar second.
- Generates a script at `/home/user/firewall.sh` containing `ufw deny from <IP>` commands for each identified malicious IP (one command per IP, no duplicates).

Requirements:
- Your log parsing must be implemented in Bash (using tools like `awk`, `grep`, `sort`, etc.).
- Ensure `/home/user/firewall.sh` is executable.

The verification process will evaluate the accuracy of the blocked IPs in your `/home/user/firewall.sh` script against the true list of malicious IPs using an F1 score metric. You must achieve an F1 score of at least 0.95.