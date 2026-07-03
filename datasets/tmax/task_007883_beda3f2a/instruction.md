You are an incident responder investigating a potential breach on a web server. The attacker appears to be bypassing the current Web Application Firewall (WAF) by double-encoding their malicious payloads. Additionally, the web server's Content Security Policy (CSP) is misconfigured, and the evidence directory has been left with insecure permissions.

Your objective is to secure the environment, analyze the logs by writing a custom C tool, and propose a hardened CSP.

Here are your instructions:

1. **Access Control**: 
   The directory `/home/user/incident/evidence/` currently has overly permissive permissions. Secure it by changing its permissions so that only the owner has read, write, and execute access (no access for group or others).

2. **Payload Decoding and Automated Scanning (in C)**:
   Inside the evidence directory, there is a log file located at `/home/user/incident/evidence/requests.log`. Each line is formatted as `IP_ADDRESS|ENCODED_PAYLOAD`. 
   The payloads have been encoded twice: first URL-encoded, and then Base64-encoded.
   
   Write a C program at `/home/user/incident/scanner.c` that does the following:
   - Reads `/home/user/incident/evidence/requests.log`.
   - Base64-decodes the payload section.
   - URL-decodes the resulting string.
   - Scans the fully decoded string for known malicious signatures. A payload is considered malicious if it contains the exact substring `<svg onload=` or `SELECT * FROM`.
   - You may use standard C libraries. Do not use external libraries (like libcurl or openssl) for the decoding; implement the decoding logic or use standard POSIX functions.

3. **Content Security Policy Enforcement**:
   The current CSP configuration is stored in `/home/user/incident/csp_policy.txt`. It currently allows inline scripts, which is dangerous.
   Update the string inside `/home/user/incident/csp_policy.txt` to enforce a strict policy:
   - `default-src` must be restricted to `'self'`.
   - `script-src` must allow only `'self'` and the specific nonce `'nonce-r4nd0m123'`. 
   - Remove any `unsafe-inline` or `unsafe-eval` directives.
   Ensure the directives are separated by semicolons and a single space.

4. **Reporting**:
   Run your C program and compile your findings. Create a final report at `/home/user/incident/report.txt` with exactly the following format:

   ```
   Evidence Secured: Yes
   Malicious Payloads:
   [IP_ADDRESS] - [DECODED_PAYLOAD]
   ...
   Fixed CSP: [YOUR_EXACT_CSP_STRING]
   ```
   *(List each malicious payload you found on a new line, keeping the exact format above. Do not include benign requests.)*