You are tasked with debugging and securing a multi-service log ingestion pipeline. 

The pipeline consists of Nginx (serving traffic), Redis (acting as a message queue), and a Python analyzer. A bash script (`/app/log_ingest.sh`) tails the Nginx access logs and pushes them into a Redis list named `raw_logs`. The Python analyzer (`/app/analyzer.py`) consumes these logs.

Currently, the system is failing on multiple fronts:
1. **Multi-Service Composition Failure:** Nginx fails to start due to a syntax error in its configuration. Furthermore, `log_ingest.sh` is trying to connect to the wrong Redis port, and the end-to-end flow is completely broken.
2. **Adversarial Payloads:** When exposed to the internet, attackers send malicious payloads (SQL injection, XSS, Path Traversal, and invalid UTF-8 byte sequences). These payloads crash our downstream analyzer and cause convergence failures in our statistical anomaly detection algorithms.

Your objectives:
1. **Fix the multi-service setup:** 
   - Identify and fix the misconfiguration in Nginx (located at `/etc/nginx/nginx.conf` or included files) so it binds correctly to port 8080.
   - Fix `/app/log_ingest.sh` so it connects to the standard Redis port (6379) instead of the erroneous 6380.
   - Ensure the pipeline can successfully route a standard curl request: Nginx -> access.log -> log_ingest.sh -> Redis.

2. **Create a Log Sanitizer (Adversarial Defense):**
   - Write a Bash script at `/app/sanitizer.sh`.
   - It must read Nginx log lines from `stdin` and write to `stdout`.
   - If a log line is clean, it must output the line exactly as it was received.
   - If a log line contains malicious patterns—specifically directory traversal (`../` or `%2e%2e`), SQL injection keywords (e.g., `UNION SELECT`, `OR 1=1`), XSS tags (e.g., `<script>`), or invalid UTF-8 bytes—the script must DROP the line entirely (output nothing for that line).
   - Integrate your sanitizer into the `/app/log_ingest.sh` pipeline so that Nginx logs are piped through `/app/sanitizer.sh` before being sent to Redis.

Our automated testing will verify your `/app/sanitizer.sh` script against two hidden corpora:
- A directory of "clean" Nginx log files. Your script must preserve 100% of these lines unchanged.
- A directory of "evil" log files containing malicious payloads. Your script must reject (output nothing) 100% of these lines.

Ensure the system services are correctly configured and your `sanitizer.sh` acts as a perfect filter for the adversarial test cases.