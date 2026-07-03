You are acting as a security auditor for a web application stack. You have two main objectives: correctly configuring a multi-service reverse proxy stack to use TLS, and writing a Bash-based security filter to block open redirect and privilege escalation payloads.

**Part 1: Multi-Service TLS Setup**
A backend Python HTTP service is located at `/app/backend.py`. This service runs on `127.0.0.1:8080` when started.
You must configure an Nginx reverse proxy to sit in front of this backend:
1. Generate a self-signed TLS certificate and private key using `openssl` (use RSA 2048, SHA256). Save them as `/home/user/cert.pem` and `/home/user/key.pem`.
2. Create an Nginx configuration file at `/home/user/nginx.conf`. It must:
   - Run entirely in user-space without root privileges (you are user `user`).
   - Listen on `127.0.0.1:8443` using HTTPS with the certificate and key you generated.
   - Proxy all incoming requests to the backend at `http://127.0.0.1:8080`.
   - Store all Nginx temporary files, PIDs, and logs inside `/home/user/nginx_data/` (you will need to create this directory and configure `pid`, `access_log`, `error_log`, and all `*_temp_path` directives to point inside it to avoid permission errors).
3. Start the backend service and start Nginx using your configuration (`nginx -c /home/user/nginx.conf`). They must remain running in the background.

**Part 2: Security Filter (Adversarial Corpus)**
The application is vulnerable to open redirects and command injection (privilege escalation). You must write a robust Bash script at `/home/user/filter.sh` to sanitize incoming request URIs.
- The script will be invoked with a single argument containing a URI path (e.g., `bash /home/user/filter.sh "/login?redirect=/dashboard"`).
- **Clean paths:** Valid paths start with a single `/`. They may contain alphanumeric characters, `_`, `-`, `.`, and standard query parameter characters (`?`, `=`, `&`).
- **Evil paths (Open Redirects):** Any payload where a redirect parameter points to an external domain (e.g., `http://`, `https://`, or protocol-relative `//`).
- **Evil paths (Privilege Escalation / Command Injection):** Any payload containing shell metacharacters that could be used for execution (`` ` ``, `$()`, `;`, `|`, `<` , `>`) or keywords indicating privesc (e.g., `sudo`, `/bin/bash`, `etc/shadow`, `/root`). 
- Your script must exit with status code `0` if the payload is safe (clean), and exit with status code `1` if it detects malicious patterns (evil).

The automated verifier will test your script against two strict corpora:
- Clean corpus: `/app/corpus/clean.txt`
- Evil corpus: `/app/corpus/evil.txt`

To succeed, you must ensure both services are actively running and correctly proxying traffic end-to-end (`curl -k https://127.0.0.1:8443/`), and your `filter.sh` must successfully classify 100% of the clean corpus as exit code 0 and 100% of the evil corpus as exit code 1.