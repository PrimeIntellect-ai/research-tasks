You are acting as a DevSecOps engineer to enforce policy as code and fix a vulnerable file upload handler. A multi-service application environment resides in `/app/`, consisting of three interacting services:
1. `nginx` (acting as the front-end TLS termination proxy on port 8443)
2. `bash-cgi` (the backend upload handler running via socat on port 8080)
3. `clamav-daemon` (a local anti-virus scanning service running on a UNIX socket at `/var/run/clamav/clamd.ctl`)

Currently, the backend upload handler is susceptible to CWE-22 (Path Traversal), allowing users to upload files outside the designated `/var/uploads/` directory.

Your task is to implement a strict Bash-based Web Application Firewall (WAF) script at `/home/user/waf.sh` that will intercept traffic between `nginx` and `bash-cgi`. This script must act as a filter that guarantees malicious path traversals are blocked and valid requests are securely forwarded.

Requirements for `/home/user/waf.sh`:
1. It must read raw HTTP headers and the POST body from standard input.
2. It must extract the requested `filename=` parameter from the `Content-Disposition` header.
3. If the filename contains any directory traversal sequences (e.g., `../`, `..%2F`, `%2e%2e%2f`) or attempts to use absolute paths (`/etc/passwd`), the script must immediately exit with code `403` and print "HTTP/1.1 403 Forbidden" to stdout.
4. If the file is allowed, the script must compute the SHA-256 hash of the uploaded payload.
5. The WAF must output "HTTP/1.1 200 OK", followed by the sanitized filename and the SHA-256 hash format: `OK: [filename] [sha256]`.
6. Ensure the script handles execution natively (needs `chmod +x`).

You must also correct the environment's configuration:
1. Fix the permissions of the `/var/uploads/` directory so only the `www-data` group can write to it, setting the SGID bit so all new files inherit the group.
2. Validate the certificate chain in `/app/certs/`. The frontend `nginx` is using `server.crt`. Verify it against `ca.crt`. If the certificate is invalid or expired, generate a new valid self-signed certificate and replace it.
3. Reconfigure the `nginx.conf` file in `/app/config/` to proxy traffic to your new WAF script via a custom spawned FastCGI wrapper on port 9000, instead of directly to port 8080.

Ensure your script is robust. An automated testing suite will fuzz your `/home/user/waf.sh` with thousands of malicious and benign payload headers to ensure it is bit-for-bit identical in behavior to our internal secure oracle.