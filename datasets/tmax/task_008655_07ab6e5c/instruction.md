You are a Site Reliability Engineer responsible for monitoring staged deployments. 

A new release is ready, and the deployment team has provided a shell script at `/home/user/rollout.sh` to trigger it. However, the script is interactive and requires manual input. Furthermore, after the deployment, you need to verify the service's health via an HTTPS endpoint and generate a notification email.

Write a Python script at `/home/user/check_deploy.py` that automates this entire process. You may use standard library modules and `pexpect`, `requests`, or `urllib`.

Your Python script must perform the following actions exactly:

1. **Interactive Deployment (Expect Scripting):**
   - Use `pexpect` to spawn `/home/user/rollout.sh`.
   - The script will prompt: `Target environment (dev/staging/prod):` -> Your script must send `staging`.
   - The script will then prompt: `Confirm staged rollout? [y/N]:` -> Your script must send `y`.
   - Wait for the `rollout.sh` script to finish executing.

2. **TLS Web Server Verification:**
   - Once the rollout script finishes, it will have started a local web service on `https://127.0.0.1:8443`.
   - Make an HTTPS GET request to `https://127.0.0.1:8443/api/status`. The server uses a self-signed certificate, so you must explicitly ignore/disable TLS certificate validation in your request.
   - Parse the JSON response.

3. **Logging:**
   - Create a log file at `/home/user/deploy_monitor.log`.
   - Write the exact following lines to the log file (replace the bracketed placeholders with actual values):
     ```
     ENV: staging
     ROLLOUT: confirmed
     HTTP_CODE: [the integer HTTP status code received]
     UPTIME_STATUS: [the string value of the "status" field from the JSON response]
     ```

4. **Email Notification Construction:**
   - If the HTTP status code is 200 and the JSON `status` is exactly `"healthy"`, generate an RFC 822 compliant email file at `/home/user/notify.eml`.
   - The file must contain exactly:
     ```
     From: sre@company.local
     To: admin@company.local
     Subject: Staging Rollout Status
     
     Deployment successful. Service is healthy.
     ```

Run your Python script to complete the deployment and generate the log and email files. Ensure both `/home/user/deploy_monitor.log` and `/home/user/notify.eml` exist and are formatted correctly before completing the task.