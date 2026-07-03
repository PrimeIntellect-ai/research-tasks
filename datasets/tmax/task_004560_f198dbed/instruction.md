You are a forensics analyst investigating a compromised host. The attacker deployed a custom multi-service command and control (C2) stack and an evidence obfuscation tool. Your goal is to reconfigure the stack to capture its end-to-end communication, reimplement the obfuscator for further analysis, and identify vulnerabilities in the malware's code.

**Part 1: Service Reconfiguration (Multi-Service Compose)**
The attacker's stack consists of Nginx, a Flask application, and Redis. The startup script `/app/start_services.sh` launches them, but the configuration files are incomplete or incorrect, preventing the services from communicating.
- Nginx config: `/app/nginx/nginx.conf`
- Flask app: `/app/flask/app.py` (reads environment variables from `/app/flask/.env`)
- Redis config: `/app/redis/redis.conf`

Your tasks for Part 1:
1. Reconfigure the services so that Nginx listens on `https://127.0.0.1:8443` (using the certificates in `/app/certs/nginx.crt` and `/app/certs/nginx.key`) and proxies requests to the Flask app on `127.0.0.1:5000`.
2. Fix the Flask app's `.env` and Redis configuration so Flask can successfully connect to Redis and authenticate.
3. Once running, a `POST` request to `https://127.0.0.1:8443/log` with a JSON payload `{"data": "test"}` should successfully pass through Nginx to Flask and be stored in Redis. (You can test this yourself using `curl -k`).

**Part 2: Cryptographic Hashing and Obfuscation (Fuzz Equivalence)**
The attacker used a stripped binary `/app/payload_obfuscator` to hash and obfuscate evidence before exfiltration. We recovered a pseudocode dump of this binary at `/app/obfuscator_pseudo.c`.
You must write a bit-exact equivalent program in Python at `/home/user/reconstructed_hasher.py`.
- Your Python script must read raw binary data from standard input (`sys.stdin.buffer.read()`).
- It must output the exact obfuscated binary data to standard output.
- It must perfectly match the behavior of `/app/payload_obfuscator` for any input.

**Part 3: Certificate Validation and Vulnerability Analysis**
1. The attacker left a certificate chain in `/app/certs/client_chain.pem`. One of the intermediate certificates is invalid/revoked based on the CRL located at `/app/certs/malware_crl.pem`. Identify the serial number of the revoked certificate and write it to `/home/user/revoked_serial.txt` (in uppercase hex format, e.g., `1A2B3C`).
2. Audit the Flask application code (`/app/flask/app.py`). It contains a specific cryptographic or authentication flaw related to how it processes incoming requests. Identify the most appropriate CWE (Common Weakness Enumeration) ID for this vulnerability and write it to `/home/user/cwe.txt` (Format: `CWE-XXX`).

Ensure all requested files are created in the exact locations specified.