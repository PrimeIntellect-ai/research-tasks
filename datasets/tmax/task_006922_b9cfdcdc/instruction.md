You are an observability engineer tasked with tuning our dashboard alerts. We have a backend metrics service that is only accessible via an SSH tunnel, and we need a custom Go-based reverse proxy to fetch metrics, evaluate them against a configuration file, and send an email alert if thresholds are exceeded.

Please complete the following tasks:

1. **SSH Tunnel Setup:**
   Generate an SSH keypair (no passphrase) and authorize it for the current user (`user`) on `localhost` so you can SSH without a password.
   Establish a local port forwarding SSH tunnel that listens on `127.0.0.1:9090` and forwards to `127.0.0.1:8080`. Keep this tunnel running in the background.

2. **Configuration File:**
   Create a configuration file at `/home/user/proxy/config.json` with the following exact content:
   ```json
   {
     "target_url": "http://127.0.0.1:9090",
     "alert_threshold_cpu": 85,
     "smtp_server": "127.0.0.1:1025",
     "alert_email": "alerts@dashboard.local"
   }
   ```

3. **Go Reverse Proxy & Alerter:**
   Write a Go program at `/home/user/proxy/main.go` and build it to `/home/user/proxy/proxy_server`.
   The Go program must:
   - Read the `/home/user/proxy/config.json` file.
   - Start an HTTP server listening on `127.0.0.1:7070`.
   - When it receives a `GET` request on `/api/metrics`:
     a. It must forward the request to the `target_url` defined in the config (which goes through your SSH tunnel to the backend).
     b. Read the JSON response from the backend. The backend will return a JSON object like `{"cpu_usage": 92, "memory_usage": 45}`.
     c. Pass the raw JSON response back to the original client.
     d. If the `cpu_usage` integer value in the response is strictly greater than `alert_threshold_cpu`, send an email using standard unauthenticated SMTP to the `smtp_server`.
        - The email 'From' address must be: `proxy@dashboard.local`
        - The email 'To' address must be the `alert_email` from the config.
        - The subject must be: `High CPU Alert`
        - The body must be: `CPU usage is at X%` (where X is the actual usage).
     e. If an alert is triggered, append a single line to `/home/user/proxy/alert.log` in the exact format: `ALERT TRIGGERED: cpu=X` (where X is the cpu_usage value).

4. **Testing:**
   Before you finish, ensure your Go proxy is running in the background. 
   Then, execute a `curl http://127.0.0.1:7070/api/metrics` to test the flow. The backend is already set up and running on port 8080. It will return a CPU usage of 95, which should trigger the alert and the log entry.