You are acting as a deployment engineer rolling out a new update mechanism. I need you to create an automated deployment system using Python that handles file operations, logging, email notifications, and scheduling.

Please perform the following steps:

1. Write a Python script located at `/home/user/deploy.py`. 
This script must perform the following actions when executed:
- Verify that the directory `/home/user/staging` exists. If it does not, the script must exit with a status code of 1.
- Move all files currently in `/home/user/production` to `/home/user/backup`. (Create `/home/user/backup` if it doesn't exist).
- Copy all files from `/home/user/staging` into `/home/user/production`.
- Append a JSON object to a log file at `/home/user/deploy_log.json`. The JSON object must be on a single new line and have exactly this schema:
  `{"status": "success", "files": ["<list_of_filenames_copied>"], "timestamp": <current_unix_timestamp_as_float>}`
- Send an email notification using Python's built-in `smtplib`. The email must be routed to the local SMTP server at `127.0.0.1` on port `1025`. 
  - The envelope sender (From) must be `deploy@company.local`.
  - The recipient (To) must be `eng-mailing-list@company.local`.
  - The email subject must be exactly `Deployment Update`.
  - The body of the email must be exactly `New release deployed successfully.`.

2. Create a cron configuration file.
Write a valid crontab line into a file named `/home/user/schedule.cron`. 
The cron job must be scheduled to execute the `/home/user/deploy.py` script using `/usr/bin/env python3` exactly at 2:15 AM every Sunday. 

Ensure your Python script is executable and handles the required steps robustly.