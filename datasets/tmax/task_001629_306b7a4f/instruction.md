Hello, our FinOps team is trying to optimize our cloud storage and compute costs. We have a telemetry stack that is currently broken, and our storage is filling up with unneeded legacy backup and log artifacts. We need you to fix the stack and create an automated cleanup script.

First, fix the telemetry stack located in `/home/user/app/telemetry_stack`. It consists of an Nginx reverse proxy, a Python Flask API, and a Redis backend. 
- Nginx should be listening on port 8080 and route requests from `/api/` to the Flask app.
- The Flask app runs on port 5000 and needs to connect to Redis.
- Redis is running on port 6379.
Currently, when a POST request is sent to `http://localhost:8080/api/record`, it fails. Please reconfigure Nginx, the Flask environment variables (located in `/home/user/app/telemetry_stack/.env`), and the startup script `/home/user/app/telemetry_stack/start.sh` so that the end-to-end flow works.

Second, we need to clean up our storage. We have a mixture of critical compliance logs and wasteful legacy backups stored in various directories. You need to write a Python script at `/home/user/app/finops_cleaner.py` that takes a directory path as a command-line argument and processes all `.log` and `.bak` files inside it.
- Your script must delete "wasteful" files and preserve "compliance" files.
- A file is considered "wasteful" (and should be deleted) if it contains the string "DEBUG_LEVEL=" OR if it is older than 30 days based on its filename (format: `app-YYYY-MM-DD.log` or `backup-YYYY-MM-DD.bak` - assume today is `2024-05-15`).
- A file is considered "compliance" (and must be kept) if it contains the string "AUDIT_TRAIL=true" (even if it has a DEBUG_LEVEL or is old, AUDIT_TRAIL takes precedence) or if it doesn't meet the wasteful criteria.

Your script must accept exactly one argument: the path to process. E.g., `python3 /home/user/app/finops_cleaner.py /home/user/data/logs`.

Finally, schedule a cron job for the current user that runs your script on the `/home/user/production_logs` directory every day at 2:00 AM.