You are acting as a capacity planner analyzing resource usage for an internal web service. You have been provided with a sample log file at `/home/user/app_logs/access.log`. The logs use a standard combined-like format where the first field is the IP address and the tenth field (after the status code) is the number of bytes transferred.

You need to complete the following system administration tasks:

1. **Resource Analysis**: Process `/home/user/app_logs/access.log` to calculate the total bytes transferred per IP address. Write the top 3 IP addresses with the highest bandwidth usage to `/home/user/capacity_report.txt`. The format of this file must be exactly three lines, each containing `IP: BYTES` sorted in descending order of bytes.

2. **TLS Preparation**: We will serve this report via a secure local dashboard soon. Generate a self-signed RSA (2048-bit) TLS certificate and private key. Save them as `/home/user/certs/cert.pem` and `/home/user/certs/key.pem` respectively. The certificate should be valid for at least 365 days. No password should be set on the private key.

3. **Log Rotation & Backup Script**: Create an executable bash script at `/home/user/backup_logs.sh`. When executed, this script must:
   - Compress `/home/user/app_logs/access.log` using `gzip`.
   - Move the compressed file to `/home/user/backup/access_$(date +%F).log.gz`.
   - Empty (truncate to zero bytes) the original `/home/user/app_logs/access.log` file so the application can continue writing to it.

4. **Scheduling**: Configure the current user's crontab to execute `/home/user/backup_logs.sh` every day exactly at midnight (00:00 server time).

Ensure all created files are placed in their precise absolute paths.