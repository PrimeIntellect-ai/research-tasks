You are a penetration tester performing a security audit on an offline backup of a web application. The backup is located in `/home/user/webapp`. You need to perform several security tasks using Bash and command-line tools. Store all your results in the `/home/user/audit` directory, which you must create.

Perform the following tasks:

1. **Certificate Analysis**:
   The directory `/home/user/webapp/certs/` contains `server.crt` and `server.key`. Verify that they are a valid pair. Extract the SHA256 fingerprint of the certificate (`server.crt`) and save it exactly as it is output by OpenSSL to `/home/user/audit/cert_fingerprint.txt` (e.g., `SHA256 Fingerprint=XX:XX:...`).

2. **File Integrity Verification**:
   The file `/home/user/webapp/checksums.txt` contains expected SHA256 hashes for the files in `/home/user/webapp/web_root/` (in the format `hash  filename`). Check the current files in the `web_root` directory against these hashes. Identify any files that have been tampered with (their current hash does not match the expected hash). Write the base filenames (e.g., `script.js`) of the tampered files, one per line, to `/home/user/audit/tampered_files.txt`.

3. **Sensitive Data Redaction**:
   The web server log file `/home/user/webapp/logs/access.log` contains HTTP request records. Some of these URIs contain sensitive query parameters: `password`, `token`, and `ssn`. Write a Bash script at `/home/user/audit/redact.sh` that reads `/home/user/webapp/logs/access.log`, replaces the values of these specific query parameters with `[REDACTED]`, and outputs the redacted log to `/home/user/audit/clean_access.log`.
   For example, `GET /api/login?username=admin&password=secret123&token=abc HTTP/1.1` should become `GET /api/login?username=admin&password=[REDACTED]&token=[REDACTED] HTTP/1.1`.
   Ensure the script is executable and run it to generate `clean_access.log`.

4. **Network Policy Generation**:
   Analyze the original `/home/user/webapp/logs/access.log`. Find the IP addresses that have generated HTTP 404 errors. Identify the top 3 IP addresses with the most 404 errors. Create a bash script at `/home/user/audit/block_ips.sh` containing exactly three `iptables` commands to drop traffic from these IPs. The format for each line must be exactly: `iptables -A INPUT -s <IP> -j DROP`. List them in descending order of their 404 error frequency.

Ensure all outputs strictly follow the specified formats.