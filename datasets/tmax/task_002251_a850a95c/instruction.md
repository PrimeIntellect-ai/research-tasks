You are tasked with fixing a broken multi-service deployment and implementing a security filter for an application.

The system consists of three services: Nginx, a Flask backend, and a Redis database. The deployment is currently broken, and the application is exposed to malicious payloads.

Your objectives are:

1. **Fix the Multi-Service Deployment:**
   - Nginx is configured to run on port 8080, but its configuration file at `/home/user/nginx/nginx.conf` is missing the upstream routing. Configure it to proxy requests from `http://127.0.0.1:8080/api/` to the Flask backend running on `http://127.0.0.1:5000/`.
   - The Flask app uses a symlink-based deployment. Update the symlink `/home/user/deploy/current` to point to `/home/user/deploy/v2` instead of the broken `v1`.
   - The Flask app requires the environment variable `REDIS_HOST` to connect to Redis (running on `127.0.0.1:6379`). Modify the startup script `/home/user/deploy/current/start.sh` to export `REDIS_HOST=127.0.0.1` before starting the app.
   - Start Nginx, Redis, and the Flask app. Ensure that a GET request to `http://127.0.0.1:8080/api/health` returns `{"status": "ok", "redis": "connected"}`.

2. **Develop a WAF Payload Detector:**
   - Write a Python script at `/home/user/waf_detector.py` that takes a single file path as a command-line argument.
   - The file will contain raw HTTP request payloads (headers and body).
   - Your script must analyze the file and print exactly `EVIL` to standard output if the payload contains signs of Path Traversal (e.g., `../`), SQL Injection (e.g., `UNION SELECT`, `' OR 1=1`), or Cross-Site Scripting (e.g., `<script>`). 
   - If the payload is benign, it must print exactly `CLEAN`.
   - You must handle variations in case (e.g., `union select` is also evil).
   - A set of examples to guide you is located in `/home/user/corpora_sample/`.

3. **Scheduled Log Monitoring:**
   - Create a bash script at `/home/user/monitor_logs.sh` that uses text processing (like `awk` or `grep`) to extract all IP addresses from `/home/user/nginx/access.log` that have received a 403 or 500 status code.
   - Set up a user-level cron job (using `crontab -e`) to run this script every 5 minutes and append the output to `/home/user/suspicious_ips.txt`.

Ensure all services are running and your `waf_detector.py` script is fully functional. Automated tests will evaluate your detector against a hidden corpus of clean and evil payloads.