You are acting as a security engineer tasked with rotating credentials and hardening a multi-service application stack. The stack consists of an Nginx reverse proxy, a Python Flask API, and a Redis backend. 

Currently, the stack is running with weak, expired TLS certificates, an old Redis password, missing security headers, and the Flask application is running without proper process isolation.

Your goal is to harden the environment located at `/app/services/` by completing the following steps:

1. **TLS/SSL Certificate Management:**
   Generate a new self-signed RSA 4096-bit certificate and private key. Place them in `/app/services/nginx/certs/server.crt` and `/app/services/nginx/certs/server.key`. The certificate must be valid for exactly 365 days. Update `/app/services/nginx/nginx.conf` to use these new certificates and configure Nginx to only accept TLSv1.2 and TLSv1.3.

2. **Content Security Policy Enforcement:**
   Modify `/app/services/nginx/nginx.conf` to include the following strict CSP header in its HTTP responses:
   `Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted.cdn.com; frame-ancestors 'none';`

3. **Credential Rotation:**
   The current Redis password is `old_secret_pass`. Generate a new, secure 16-character alphanumeric password. Update both the Redis configuration (`/app/services/redis/redis.conf`) and the Flask application (`/app/services/flask/app.py` or its environment variables, depending on how `start.sh` is structured) to use this new password. The old password must no longer work.

4. **Process Isolation and Sandboxing:**
   Modify the application startup script (`/app/services/start.sh`) to run the Flask application using `bwrap` (Bubblewrap) for sandboxing. The Flask application must run with an unshared PID namespace (`--unshare-pid`), read-only access to the root filesystem (`--ro-bind / /`), read-write access to `/tmp` (`--bind /tmp /tmp`), and it must share the host network (`--share-net`) so it can communicate with Redis and Nginx.

You can start the services by running `/app/services/start.sh`.

We will verify your setup using an automated grading script located at `/app/verifier/score.py`. This script connects to the services, verifies the TLS certificates, checks the CSP headers, tests the end-to-end API flow to ensure the Flask app can still reach Redis with the new password, and verifies the sandbox. 

You must achieve a security score of 95 or higher (out of 100) from `/app/verifier/score.py`. Write a final log file to `/home/user/rotation_complete.log` containing the new Redis password once you are done.