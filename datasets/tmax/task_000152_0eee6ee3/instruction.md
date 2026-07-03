You are a security auditor assigned to evaluate the security posture of an internal application stack. The system runs locally in a restricted environment. You must perform certificate validation, exploit a vulnerable endpoint to recover sensitive data, sanitize that data, and generate network policies to block malicious actors.

**Phase 1: Certificate Chain Validation**
You have been provided with a Root Certificate Authority (CA) file located at `/home/user/ca.pem` and a directory containing several client certificates and their private keys at `/home/user/clients/`. 
Your first task is to identify the single valid client certificate in this directory. A valid certificate must:
1. Be mathematically signed by `/home/user/ca.pem`.
2. Be currently valid (not expired, and its validity period has started).
Once you find the valid certificate, note its filename (e.g., `client_N.crt`) and its associated private key (`client_N.key`).

**Phase 2: Exploit and Payload Delivery**
A local API service is running on `https://127.0.0.1:8443`. It enforces Mutual TLS (mTLS), meaning you can only interact with it if you provide the valid client certificate and key identified in Phase 1. 
The service has an endpoint `/fetch_audit?log=...` that expects a log filename. Through preliminary code review, you suspect this endpoint is vulnerable to directory traversal.
Craft a payload using standard tools (like `curl`) to authenticate via mTLS and exploit the directory traversal vulnerability to read the file located at `/home/user/service/internal_secrets.txt`.

**Phase 3: Sensitive Data Redaction**
The `internal_secrets.txt` file you extracted contains highly sensitive information, including names, departments, and credit card numbers. 
You must create a sanitized version of this file. Redact all credit card numbers (which appear as 16 digits, formatted either as `XXXX-XXXX-XXXX-XXXX` or `XXXX XXXX XXXX XXXX`) by replacing the entire credit card string with the exact text `[REDACTED]`.
Save the sanitized output to exactly: `/home/user/redacted_secrets.txt`.

**Phase 4: Network Policy Configuration**
The service access logs are stored at `/home/user/service/access.log`. Malicious bots have been brute-forcing the application.
Analyze this log file. Identify any IP addresses that have received more than 3 responses with an HTTP `403` status code.
Create an Nginx configuration snippet that blocks these malicious IPs. The file must be saved to `/home/user/nginx_block.conf` and should contain one directive per line in this exact format:
`deny <IP_ADDRESS>;`

Complete all phases and ensure the files `/home/user/redacted_secrets.txt` and `/home/user/nginx_block.conf` are perfectly formatted as requested.