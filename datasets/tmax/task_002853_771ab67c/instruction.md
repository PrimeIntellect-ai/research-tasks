You are a backup operator testing a recent restore of an internal application stack. The restored files are located in `/home/user/restore_test`. This stack consists of a backend service, a reverse proxy, a mock email server, and a health-checking daemon, all managed by `supervisord` running in user space.

Due to a configuration drift in the backed-up data, the system is failing to start properly, and services are silently failing or rejecting connections—similar to an SSH configuration silently dropping key-based logins. 

Your objectives are to diagnose, fix, and validate this restored stack.

**Phase 1: Environment Startup & Diagnosis**
1. The restored stack relies on Python's `supervisor`. Install it locally if needed (`pip install supervisor`).
2. Start the application stack using the provided configuration: `supervisord -c /home/user/restore_test/supervisord.conf`.
3. Check the supervisor logs in `/home/user/restore_test/logs/`. You will notice that the `healthcheck` service is failing to validate the backend and failing to send alert emails.

**Phase 2: Code & Configuration Fixes**
1. **Connectivity & Reverse Proxy:** The reverse proxy (`/home/user/restore_test/proxy.py`) runs on port 8080 and proxies to the backend on port 9000. It is currently silently rejecting requests from the health checker. Identify the restriction in `proxy.py` and modify it so that it accepts standard GET requests to `/ping` without requiring any special headers.
2. **Email Server Config:** The mock SMTP server runs on port 8025. The `healthcheck.py` script is misconfigured to send alert emails to the default port 25 (which requires root privileges and fails). Fix `healthcheck.py` to point to port 8025.

**Phase 3: Validation Script**
Write a Python script at `/home/user/restore_test/verify_restore.py` that performs a final end-to-end diagnostic of the restored environment. The script must:
1. Send an HTTP GET request to `http://127.0.0.1:8080/ping`.
2. Ensure the response status code is 200 and the body contains the word "PONG".
3. Connect to the mock SMTP server at `127.0.0.1:8025` and send an email from `operator@localhost` to `backup-success@localhost` with the subject "Restore Test Passed" and body "All services operational."
4. If and only if both the HTTP check and the email dispatch succeed, append the exact string "RESTORE VALIDATED" to the file `/home/user/restore_test/restore_status.txt`.

Ensure your final `verify_restore.py` script is executable and you have run it successfully at least once before completing the task.