Act as a monitoring specialist. We have a legacy application that silently fails by logging authentication rejections to a local file instead of alerting us. I need you to build a reliable monitoring pipeline.

Please complete the following steps:

1. **C++ Log Parser:** 
   Write a C++ program at `/home/user/monitor.cpp`. The program must accept two command-line arguments: an input log file path and an output alert file path.
   - It should read the input file line by line.
   - For every line containing the exact string `REJECT key_auth`, it should append an RFC-compliant email snippet to the output file.
   - The email snippet must match this exact format (including the blank line before the body):
     ```
     To: admin@localhost
     Subject: Alert - Auth Rejected
     Date: [YYYY-MM-DD HH:MM:SS]
     
     Auth failure detected.
     ```
   - The `[YYYY-MM-DD HH:MM:SS]` must be the current local time of the system running the program, formatted exactly as shown (e.g., `2024-05-12 14:30:00`).

2. **Idempotent Deployment Script:**
   Write a bash script at `/home/user/deploy.sh` that sets up the environment and service safely. The script must be completely idempotent (running it multiple times must not fail or duplicate configurations). The script must:
   - Ensure the directory `/home/user/alerts/mail_spool` exists.
   - Set strict permissions on `/home/user/alerts/mail_spool` so that ONLY the owner has read, write, and execute permissions (no permissions for group or others).
   - Compile `/home/user/monitor.cpp` using `g++` into an executable at `/home/user/monitor_bin`.
   - Create a systemd user service unit file at `/home/user/.config/systemd/user/app-monitor.service`. You do not need to start or enable the service (to accommodate container limits), but the file must be perfectly formatted and contain:
     - A `[Service]` section that executes `/home/user/monitor_bin /home/user/app.log /home/user/alerts/mail_spool/alerts.eml`.
     - A restart policy that always restarts the service, with a 3-second delay between restarts.
     - An environment variable configuration that forces the service's timezone to `Asia/Tokyo` (so the C++ program logs the time in JST).

Ensure `/home/user/deploy.sh` is executable. You do not need to create `/home/user/app.log`, as the automated tests will provide it when testing your binary.