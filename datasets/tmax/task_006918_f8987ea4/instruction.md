I am a monitoring specialist trying to set up an alert routing system, but I'm running into startup sequence issues and missing some operational configurations. 

I have a Go-based reverse proxy (`/home/user/proxy/proxy.go`) that load-balances alert webhooks to two backend receivers. Currently, a startup script (`/home/user/start_services.sh`) starts the reverse proxy in the background, and then starts the backend receivers. However, the proxy crashes immediately on startup because it performs an initial health check on the backends before they are ready (a classic missing startup dependency issue). 

Additionally, the backends write their alerts to `/home/user/alerts/alerts.log`. The permissions on this file are currently too open, and there is no log rotation configured.

Please fix the system by completing the following tasks:

1. **Robust Proxy Startup (Go):** 
   Modify `/home/user/proxy/proxy.go`. Find the `checkBackends()` function. Currently, it `panic()`s if it cannot connect to `127.0.0.1:8081` and `127.0.0.1:8082`. Update this function to implement connectivity diagnostics and retries. It should retry the connection to the backends up to 5 times, with a 1-second delay between attempts, before finally panicking. Recompile the proxy to `/home/user/proxy/proxy_bin`.

2. **Permissions:**
   Set the permissions of `/home/user/alerts/alerts.log` so that only the owner has read and write access (no permissions for group or others).

3. **Log Rotation:**
   Create a logrotate configuration file at `/home/user/logrotate.conf` specifically for `/home/user/alerts/alerts.log`. Configure it with the following exact directives:
   - Rotate daily
   - Keep 3 backups (`rotate 3`)
   - Do not emit errors if the file is missing (`missingok`)
   - Do not rotate if the file is empty (`notifempty`)

4. **Verification Script:**
   Create a bash script at `/home/user/test_alert.sh` that does the following:
   - Executes `/home/user/start_services.sh`
   - Waits 7 seconds for all services to be fully healthy
   - Sends an HTTP POST request to `http://127.0.0.1:8080/alert` with the JSON payload `{"message": "Critical CPU usage"}`
   - Writes *only* the HTTP status code of the response (e.g., `200`) into `/home/user/result.txt`.

Do not modify `/home/user/start_services.sh` or the backend source code. Fix the issue strictly by making the Go reverse proxy robust against delayed backend availability.