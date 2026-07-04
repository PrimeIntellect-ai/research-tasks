You are a capacity planner configuring a lightweight, user-space health and resource monitoring script. Since you do not have root access, you need to simulate system-level checks and prepare a secure serving mechanism for the reports.

Please complete the following objectives:

1. **Mount & fstab extraction:** There is a mock fstab file located at `/home/user/fstab_mock`. Write a Python script (or use shell commands) to parse this file and extract the exact mount point path for the filesystem with the UUID `A1B2-C3D4`.

2. **Connectivity diagnostics & Health check:** Your Python script must check the health of an internal service by sending an HTTP GET request to `http://127.0.0.1:9090/health`. If the request succeeds with an HTTP 200 status code, the status is "UP". If the connection is refused, times out, or returns any other status, the status is "DOWN".

3. **Timezone & Locale:** Generate a timestamp of the exact moment the health check is performed. The timestamp must be formatted exactly as `YYYY-MM-DD HH:MM:SS TZ` (e.g., `2023-10-25 15:30:00 JST`). The timezone MUST be `Asia/Tokyo`. 

4. **Report Generation:** Create a JSON file at `/home/user/capacity_report.json` containing the gathered data. The JSON structure must exactly match:
```json
{
  "timestamp": "<the Asia/Tokyo timestamp>",
  "target_mount": "<extracted mount point>",
  "service_status": "<UP or DOWN>"
}
```

5. **Web Server TLS Setup:** Generate a self-signed RSA-2048 TLS certificate (`/home/user/tls.crt`) and private key (`/home/user/tls.key`) valid for 365 days, with the Common Name (CN) set to `localhost`. You do not need to start the web server, but these files must be present so another process can securely serve the `capacity_report.json` over HTTPS.

You may use Bash or Python to accomplish these tasks. All resulting files (`capacity_report.json`, `tls.crt`, `tls.key`) must be saved in `/home/user`.