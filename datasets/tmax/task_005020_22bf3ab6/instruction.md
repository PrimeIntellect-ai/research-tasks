You are a Site Reliability Engineer (SRE). A recent outage was caused by processes exceeding their disk quotas, hanging, and requiring manual restarts. 

You need to write a Python script that analyzes storage metrics, generates formatted email alerts for a local mailing list, and creates a shell script containing process supervisor commands to restart the affected services.

Write a Python script at `/home/user/process_metrics.py` that does the following:

1. Reads the log file located at `/home/user/metrics.log`.
   The log file contains lines in this exact format:
   `[YYYY-MM-DD HH:MM:SS] SERVICE=<service_name> USAGE=<bytes> QUOTA=<bytes>`

2. Identifies all services where `USAGE` is strictly greater than `QUOTA`.

3. For each service exceeding its quota, appends an email block to `/home/user/mail_spool/alerts.txt`. Ensure the directory `/home/user/mail_spool/` exists. Each email block must be formatted exactly as follows, with a single blank line separating multiple emails:
   ```
   To: sre-alerts@company.local
   Subject: Quota Exceeded for <service_name>
   Body: Service <service_name> used <USAGE> bytes, exceeding quota of <QUOTA> bytes.
   ```

4. For each service exceeding its quota, appends a restart command to `/home/user/supervisor_actions.sh`. Each command should be on its own line in this format:
   ```
   supervisorctl restart <service_name>
   ```

5. After writing your Python script, execute it so the output files are generated. Ensure your script handles files appropriately and closes them.

Do not use hardcoded service names in your script; it must parse the `/home/user/metrics.log` file dynamically.