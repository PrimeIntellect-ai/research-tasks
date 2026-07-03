You are acting as a Cloud Architect migrating a set of localized backend services to a new cloud region. 

Your task is to write a single Python script at `/home/user/check_deploy.py` that handles a staged deployment diagnostic check, configures the environment's timezone, and schedules itself for continuous monitoring. 

The Python script must perform the following actions when executed:
1. **Connectivity Diagnostics:** Check TCP connectivity to `127.0.0.1` on ports `8081` (Stage 1 Database) and `8082` (Stage 2 Database). Use a timeout of 1 second for each connection attempt.
2. **Staged Deployment Status:** Generate or overwrite a JSON file at `/home/user/deploy_status.json` containing the exact keys below based on the connectivity check:
   - `"stage1"`: Set to `"ready"` if port 8081 is accepting connections, otherwise `"offline"`.
   - `"stage2"`: Set to `"ready"` if port 8082 is accepting connections, otherwise `"offline"`.
   - `"last_checked_tz"`: Hardcode the target region timezone, which must be `"Asia/Tokyo"`.
3. **Locale/Timezone Configuration (Idempotent):** Update `/home/user/.bashrc` to ensure the target timezone is exported. It must add the exact line `export TZ=Asia/Tokyo`. If this line already exists in the file, do not add it again.
4. **Scheduled Task Configuration (Idempotent):** Configure the user's crontab to run this script every 5 minutes. The cron entry must be exactly `*/5 * * * * /usr/bin/python3 /home/user/check_deploy.py`. If this exact entry is already in the crontab, do not duplicate it. (Ensure you do not delete any pre-existing cron jobs).

Once you have written the script, execute it at least once so the JSON file is generated, the `.bashrc` is updated, and the crontab is configured.