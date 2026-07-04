You are a cloud architect responsible for migrating a legacy Python microservice to a new local deployment. The migration is currently failing due to misconfigurations, and several pre-migration administrative tasks need to be completed.

Your objective is to fix the service, verify system health, and prepare the data for migration. Perform the following steps:

1. **Fix the 502 Bad Gateway Error:**
   The service consists of a Python web application running behind an unprivileged Nginx reverse proxy. You can start, stop, and restart the services using the provided wrapper script: `/home/user/service/start.sh`.
   Currently, making a request to `http://127.0.0.1:8080` returns a 502 error. 
   - Analyze the Nginx configuration located at `/home/user/service/nginx.conf`.
   - Analyze how the Python application is started inside `/home/user/service/start.sh`.
   - The issue is a mismatched Unix socket path between the reverse proxy and the application. Fix the configuration so the application binds to the correct socket path expected by Nginx. Restart the service and ensure `curl http://127.0.0.1:8080` returns a successful `200 OK` response.

2. **Access Control List (ACL) Management:**
   The migrated application will eventually be served by a centralized static file server running as the `nobody` user. 
   - Use `setfacl` to grant the user `nobody` read (`r`) and execute (`x`) permissions to the directory `/home/user/service/public`. 
   - Note: Do not change the standard owner or group of the directory; strictly use ACLs.

3. **Data Backup:**
   Before completing the migration, safely archive the legacy data.
   - Create a compressed tar archive of the `/home/user/legacy_data` directory.
   - Save the archive exactly at `/home/user/legacy_data_backup.tar.gz`.

4. **Storage Monitoring Script:**
   Write a Python script at `/home/user/storage_check.py` to monitor disk space.
   - The script must use standard Python libraries (e.g., `shutil` or `os`) to check the available free space on the `/` filesystem.
   - If the available free space is strictly greater than `1048576` bytes (1 MB), the script must write the exact string `OK` to `/home/user/storage_status.txt`.
   - If the free space is less than or equal to `1048576` bytes, it must write `FULL` to `/home/user/storage_status.txt`.
   - Run the script once so that the status file is generated.

5. **Timezone and Locale Normalization:**
   The legacy logs use UTC, but the new monitoring stack expects the Eastern Time zone.
   - Read the log file at `/home/user/events.log`. Each line contains an ISO 8601 UTC timestamp (e.g., `2023-10-01T12:00:00Z`).
   - Write a Python script at `/home/user/tz_convert.py` that reads this file and converts each timestamp to the `America/New_York` timezone.
   - The script must write the converted timestamps to `/home/user/events_ny.log` in the exact format `YYYY-MM-DD HH:MM:SS` (one per line, in the same order).
   - Run the script so the output file is generated.

Ensure all Python scripts are written in Python 3 and executed successfully.