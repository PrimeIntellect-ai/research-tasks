You are an observability engineer tasked with integrating a legacy alerting system with a modern dashboard API. The legacy system fires alerts by sending raw emails, but it has no native concept of UTC, and occasionally sends malformed spam or localized logs that crash our ingest pipeline.

You must build a resilient pipeline that catches these emails, sanitizes and normalizes them, and feeds them into the dashboard.

There are three services running on this system (started via `/app/start_services.sh`):
1. **Legacy Emitter**: Listens on TCP port 10023. It simulates the legacy application.
2. **SMTP Receiver**: A local mail sink listening on TCP port 10025.
3. **Dashboard API**: A webhook listener on TCP port 10080.

### Step 1: The Email Filter & Sanitizer (Python)
Write a Python script at `/home/user/filter.py`. This script must read a raw RFC 5322 email from `stdin`.
- If the email is a valid alert, print a JSON object to `stdout` and exit with code `0`.
- If the email is invalid, malicious, or spam, exit with code `1` (printing nothing).

**Valid Alert Rules:**
- The `Subject` header must strictly be `[ALERT] <metric_name>` (e.g., `[ALERT] memory_usage`).
- The `Date` header will be in various valid RFC 2822 formats with different timezones (e.g., `+0200`, `EST`). You must parse this and normalize the timestamp to strict UTC in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`.
- The body of the email must contain a line exactly matching: `Value: <float>`.

To ensure your filter is robust, we have provided two corpora:
- `/home/user/corpora/clean/`: Contains valid emails that your script MUST accept and parse correctly.
- `/home/user/corpora/evil/`: Contains spam, malformed headers, missing fields, and XSS injection attempts that your script MUST reject (exit code 1).

### Step 2: Service Glue
The SMTP Receiver is configured to write all incoming emails to `/home/user/incoming_mail/`.
Write a bash script at `/home/user/process_mail.sh` that:
1. Iterates through all files in `/home/user/incoming_mail/`.
2. Passes each through your `/home/user/filter.py`.
3. If the filter succeeds, `POST`s the resulting JSON payload to `http://localhost:10080/ingest` using `curl` with `Content-Type: application/json`.
4. Deletes the processed email file regardless of success or failure.

### Step 3: Expect Script Integration
You must trigger a live test of the legacy system. The system requires an interactive login to set the user's locale and timezone before it will emit an alert.
Write an Expect script at `/home/user/trigger_alert.exp` that connects to the legacy emitter (`nc localhost 10023`) and performs the following interaction:
1. Wait for `Username:`, send `admin`
2. Wait for `Password:`, send `observability`
3. Wait for `Locale:`, send `en_US.UTF-8`
4. Wait for `Timezone:`, send `Europe/Paris`
5. Wait for `> `, send `EMIT cpu_load 0.85`
6. Wait for `> `, send `QUIT`

After writing the scripts, run your expect script, and then run your `process_mail.sh` script to ensure the metric successfully lands in the dashboard.