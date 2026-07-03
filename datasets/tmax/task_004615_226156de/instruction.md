You are acting as a compliance analyst tasked with generating audit trails, securing our internal services, and investigating recent security logs. Our system consists of a Flask application backend and an Nginx reverse proxy, which are currently failing our internal compliance checks. 

The environment is set up under `/app`. You need to perform a comprehensive security remediation and forensic analysis.

Here are your objectives:

**1. TLS Certificate Management & Chain Validation**
Our Nginx service (`/app/nginx/nginx.conf`, running on port 8443) is currently serving an expired, self-signed certificate. 
We have an internal Certificate Authority (CA) located at `/app/ca/`. 
- Generate a new private key and CSR for the domain `localhost`.
- Sign this CSR using the internal CA (`/app/ca/ca.crt` and `/app/ca/ca.key`). Make the certificate valid for 30 days.
- Configure `/app/nginx/nginx.conf` to use your newly generated certificate and private key. (The Nginx process runs as the `user` account, so you can restart it by sending a `SIGHUP` or manually restarting the process).

**2. Content Security Policy (CSP) Enforcement**
Our Nginx reverse proxy does not enforce a Content Security Policy. Modify the Nginx configuration to include the following strict CSP header on all responses:
`default-src 'self'; script-src 'self' https://trusted.cdn.com; object-src 'none';`

**3. Privilege Escalation Auditing**
As part of the compliance audit, we must log any potential privilege escalation vectors in the specific bin directory provided by the vendor.
Scan the directory `/app/bin/` for any files that have the SUID bit set. 
Write the absolute paths of all discovered SUID binaries into a file at `/home/user/suid_audit.txt`, one path per line.

**4. Security Log Parsing & Correlation (Python)**
We have collected authentication logs from the application backend at `/app/logs/security.log`. The logs contain JSON entries with fields such as `timestamp` (ISO 8601), `ip_address`, `event_type` (e.g., `login_failed`, `login_success`), and `username`.
Write a Python script at `/home/user/audit_parser.py` that parses this file to detect brute-force patterns.
- An IP should be flagged as malicious if it has strictly more than 5 `login_failed` events within any rolling 60-second window.
- Your script must execute and output a JSON array of the unique malicious IP addresses to `/home/user/malicious_ips.json`. 
Example output format: `["192.168.1.10", "10.0.0.5"]`

Your final solution will be evaluated against a hidden set of true malicious IPs using an F1-score metric. You must achieve an F1-score of at least 0.95. Furthermore, an automated client will connect to `https://localhost:8443/api/status` using the internal CA to verify the certificate chain and CSP headers.