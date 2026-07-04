You are a forensics analyst tasked with recovering evidence from a compromised Linux server. We have secured the web server logs, but the attacker obfuscated their exfiltration traffic and manipulated security headers to maintain access.

The logs are located at `/home/user/evidence/server_logs.tsv`.
This file is a Tab-Separated Values (TSV) file with the following columns:
1. Timestamp
2. Source IP
3. HTTP Method
4. Request URI
5. User-Agent
6. Cookie
7. Content-Security-Policy (Response Header)

Your objectives are to analyze these logs and extract critical forensics data using any programming language or CLI tools you prefer. 

Complete the following tasks:

1. **Intrusion Detection**: The attacker used a custom automated tool for exfiltration. Identify all log entries where the `User-Agent` contains the string `X-Exfil-Agent`. Extract the unique Source IPs from these malicious requests and save them, one per line, to `/home/user/attacker_ips.txt`.

2. **CSP Vulnerability Analysis**: The attacker injected a malicious Content-Security-Policy to allow Cross-Site Scripting (XSS). Scan the entire log file and identify any entries where the `Content-Security-Policy` column contains the directive `unsafe-eval`. Extract the unique `Request URI`s associated with these misconfigured policies and save them, one per line, to `/home/user/vulnerable_uris.txt`.

3. **Payload Decoding and Cryptanalysis**:
   - The attacker exfiltrated data via the `Cookie` header in the malicious requests identified in Step 1.
   - The value of the cookie (e.g., `session=...`) contains the exfiltrated payload after the `session=` prefix.
   - The payload is obfuscated: it is first encrypted using a single-byte XOR cipher, and then Base64 encoded.
   - *Known Plaintext*: You know from memory forensics that every single exfiltrated payload begins with the exact string `EXFIL_START`.
   - Use this known plaintext to deduce the XOR key.
   - Decrypt all exfiltrated payloads from the malicious requests. 
   - Write the fully decrypted, plaintext payloads (including the `EXFIL_START` prefix), one per line, to `/home/user/recovered_payloads.txt`.

Make sure to format the output files exactly as requested (plain text, one item per line, no extra spaces or headers).