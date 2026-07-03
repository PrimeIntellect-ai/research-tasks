You are an incident responder investigating a recent web server compromise. The attacker exfiltrated logs containing Content Security Policy (CSP) violation reports, which they temporarily stored on the server in an encrypted format.

We have recovered this file at `/home/user/exfil_logs.enc`. 
Through reverse engineering the malware, we discovered that the attacker encrypted the plain text logs by applying a repeating XOR cipher with the key `INTRUSION`, and then Base64-encoded the result.

Your task consists of three parts:

1. **Decryption**: Write a Python script to decrypt `/home/user/exfil_logs.enc`. Save the plain text output to `/home/user/decrypted.log`. The decrypted file consists of JSON objects (one per line), representing CSP violation reports.
2. **Intrusion Detection**: Parse the decrypted logs and extract the `blocked-uri` field from each CSP report. We need to identify which URIs were part of the attacker's payload. A URI is considered malicious if it contains the substring `malware` or if it ends with `.exe`. 
   Save all unique malicious URIs (one per line, sorted alphabetically) to `/home/user/threats.txt`.
3. **CSP Enforcement Generation**: The remaining `blocked-uri` values (those that are NOT malicious) are actually legitimate external scripts that were blocked because the current CSP is too restrictive. Extract the protocol and domain name (e.g., `https://trusted.com`) from these legitimate blocked URIs. 
   Generate a new strict CSP header for the `script-src` directive that allows `'self'` and these legitimate domains. Save the exact header string to `/home/user/new_csp.txt` in the following format:
   `Content-Security-Policy: script-src 'self' <domain1> <domain2>;`
   (Sort the domains alphabetically, separated by a single space).

Ensure all your processing can be done with standard Python 3 libraries.