You are acting as a compliance analyst and security engineer. We have a prototype Audit Trail Pipeline running in `/app/audit_pipeline/`. This pipeline processes encrypted session cookies to generate audit logs, but it has severe configuration issues and a major security vulnerability. 

The system consists of four components:
1. **Nginx Reverse Proxy**: Listens on `127.0.0.1:8080`.
2. **Flask API**: Runs on `127.0.0.1:5000`. Receives HTTP requests and pushes audit jobs to Redis.
3. **Redis**: Runs on `127.0.0.1:6379`. Acts as a message queue.
4. **Audit Worker**: A Python daemon (`worker.py`) that reads jobs from Redis, decrypts the session cookie, and executes a legacy logging binary (`/app/audit_pipeline/bin/logger`).

**Your Objectives:**

**Part 1: Service Integration & Configuration**
The services are currently misconfigured and failing to communicate.
- Start Nginx, Redis, and the Flask API. (Config files are in `/app/audit_pipeline/config/`).
- Fix Nginx so that it correctly forwards the `Audit-Session` HTTP cookie to the Flask API. Currently, Nginx is dropping this specific cookie.
- Fix the Flask API (`/app/audit_pipeline/api.py`) so it correctly connects to Redis on the standard port and pushes the raw cookie value to the `audit_jobs` queue.

**Part 2: Remediate the Credential Leak**
The `worker.py` script pops jobs from Redis, decrypts the AES-GCM encrypted `Audit-Session` cookie (the key is stored in `/app/audit_pipeline/keys/worker.key`), and passes the decrypted credentials to the legacy `/app/audit_pipeline/bin/logger` binary.
- **Vulnerability**: The worker currently passes the decrypted plaintext credential to the binary via command-line arguments (e.g., `./logger --cred <PLAINTEXT>`). This leaks the credential to any local user via `/proc/[pid]/cmdline`.
- **Fix**: Modify `/app/audit_pipeline/worker.py` to securely pass the decrypted credential to the `logger` binary via `stdin` instead of command-line arguments. The `logger` binary has been updated to accept credentials via `stdin` if the `--read-stdin` flag is provided.

**Part 3: Historical Audit Log Classifier**
Because of the previous vulnerability, we have a large batch of historical process execution logs in `/app/corpora/`. Some of these logs contain leaked credentials or malicious privilege escalation commands injected by attackers exploiting the leak.
- Write a Python script at `/home/user/classifier.py` that acts as a log sanitization filter.
- The script must take a single command-line argument: the path to a directory of log files.
- For each `.log` file in the directory, your script must read the JSON contents (which represent process execution events) and determine if the log is "clean" or "evil".
- A log is "evil" if it contains command-line arguments revealing the sensitive session format (matching `SESSION_SEC_[A-Z0-9]{16}` in the `cmdline` field) OR if the `uid` transitioning indicates an unauthorized privilege escalation (a process spawned by `uid` > 1000 executing `sudo` or `su` without a corresponding authorized `tty` context).
- For each file, print exactly one line to `stdout` in the format: `<filename>: CLEAN` or `<filename>: EVIL`.

Ensure all services are running and correctly glued together. Once complete, leave the Flask API, Redis, and Nginx running.