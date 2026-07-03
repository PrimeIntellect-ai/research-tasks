You are acting as a Site Reliability Engineer (SRE). Our internal monitoring dashboard has gone down, and the raw uptime logs are being flooded with anomalous, malformed requests. 

You need to accomplish two main objectives to restore the system:

**Part 1: Restore the Monitoring Pipeline (Service Composition & Tunneling)**
We have three services located in `/home/user/monitoring_stack/`:
1. A Redis instance used for caching metrics.
2. A Python API (Flask) that provides uptime metrics.
3. An Nginx reverse proxy.

Currently, they are misconfigured. You must:
- Update `/home/user/monitoring_stack/nginx.conf` so that Nginx listens on port `8080` and proxies all `/api/` requests to the Python API running on `127.0.0.1:5000`.
- Update `/home/user/monitoring_stack/api/.env` to configure the Python API to connect to Redis on `127.0.0.1:6379`.
- Start all three services in the background. (You can run `redis-server /home/user/monitoring_stack/redis.conf &`, Nginx with `nginx -c /home/user/monitoring_stack/nginx.conf &`, and the API via `python3 /home/user/monitoring_stack/api/app.py &`).
- Once the stack is up, you must create a persistent SSH tunnel. Our remote metric aggregator expects to pull metrics from local port `9000`. Set up an SSH tunnel that forwards local port `9000` to the Nginx port `8080` via `localhost`. (Assume you have passwordless SSH access to `user@localhost`). Leave this tunnel running in the background.

**Part 2: Log Sanitization Filter (Adversarial Corpus)**
Our uptime logs are being polluted with malicious requests (e.g., SQL injections, path traversals, XSS attempts) masquerading as monitoring checks. 
You must write a Bash script at `/home/user/sanitize_logs.sh` that takes a single log file as an argument and outputs the sanitized logs to `STDOUT`.

The script must:
- Use standard bash tools (awk, sed, grep).
- Preserve 100% of legitimate monitoring requests. A legitimate request typically looks like an HTTP GET request to `/api/health` or `/api/metrics` returning a 200 status code, from standard monitoring user agents.
- Completely filter out (reject) any log line containing malicious payloads, anomalies, or invalid HTTP methods.

To help you develop this script, two sample directories are provided:
- `/home/user/corpus/clean/`: Contains examples of perfectly clean monitoring logs.
- `/home/user/corpus/evil/`: Contains examples of malicious log lines that MUST be dropped.

Your script will be automatically tested against a hidden corpus of clean and evil logs. It must drop exactly the evil lines and retain exactly the clean lines. Make sure your script is executable (`chmod +x`).