You are a monitoring specialist tasked with setting up an alert system for a simulated microservices environment. Three backend services are currently running on your local machine on ports 8001, 8002, and 8003. However, they are experiencing intermittent network misconfigurations, and you need to monitor their health. 

You must complete the following phases to set up a secure alerting pipeline entirely within `/home/user/`.

**Phase 1: Secure Webhook Receiver (TLS Configuration)**
1. Generate a self-signed RSA 2048-bit certificate (`cert.pem`) and private key (`key.pem`) in `/home/user/webhook/` (valid for 365 days, with the Common Name `localhost`).
2. Write a Python script at `/home/user/webhook/server.py` that implements a simple HTTPS webhook server listening on `127.0.0.1` port `8443`.
3. The server must use the generated `cert.pem` and `key.pem` for TLS.
4. When the server receives a `POST` request to `/alert`, it must read the JSON payload and append the raw JSON string followed by a newline to `/home/user/webhook/alerts.log`. It should respond with a 200 OK.
5. Start this Python server in the background.

**Phase 2: Bash Monitoring Script**
1. Write a Bash script at `/home/user/monitor.sh`.
2. The script must check the health of the three services by sending an HTTP GET request to `http://127.0.0.1:<port>/health` for ports 8001, 8002, and 8003.
3. If a service does not return an HTTP 200 OK status code (e.g., it returns 503 or fails to connect), the script must trigger an alert.
4. To trigger an alert, the script must send an HTTP POST request to your secure webhook receiver at `https://127.0.0.1:8443/alert`. 
5. The POST request must ignore SSL verification errors (since you used a self-signed cert) and send exactly this JSON payload format: `{"service": "service_<port>", "status": "down"}` (e.g., `{"service": "service_8003", "status": "down"}`).
6. Ensure `/home/user/monitor.sh` is executable.

**Phase 3: Automation & Testing**
1. Create a crontab configuration file at `/home/user/cron.conf` that schedules `/home/user/monitor.sh` to run every minute (`* * * * *`). Load this file into the current user's crontab.
2. Manually execute `/home/user/monitor.sh` exactly once to test the pipeline and populate the log file immediately.

*Note: You do not need root access for any of these steps. The 3 backend services are already running.*