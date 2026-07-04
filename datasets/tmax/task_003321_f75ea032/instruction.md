You are an incident responder investigating a potential server compromise. A suspicious web log, a directory of system binaries, and a set of certificates have been captured and placed in `/home/user/incident/`.

Your objective is to analyze the artifacts using Bash utilities and compile your findings into a report.

Follow these steps:
1. **Security Log Parsing & Decoding:** Read `/home/user/incident/web.log`. Find the HTTP request originating from the IP address `192.168.1.100` that resulted in a `200` HTTP status code. Extract the base64-encoded string from the `X-Malware-Drop` HTTP header of this specific request. Decode the base64 string.
2. **Privilege Escalation Auditing:** The decoded payload from step 1 contains the name of a target executable in the format `target_bin=<filename>`. Search the `/home/user/incident/bin/` directory for this specific filename. Verify if this file has the SUID bit set.
3. **Certificate Validation:** The attacker left behind a certificate at `/home/user/incident/certs/implant.pem`. Use OpenSSL to verify if this certificate is validly signed by the Certificate Authority at `/home/user/incident/certs/rootCA.pem`. Also, extract the Common Name (CN) of the `implant.pem` certificate subject.

Compile your final findings into a log file at `/home/user/report.txt` with the following exact format (one per line):
PAYLOAD_DECODED=<the exact decoded string from step 1>
SUID_BIN_PATH=<the absolute path to the targeted SUID binary found in step 2>
CERT_VALID=<YES if the certificate is validly signed by rootCA.pem, otherwise NO>
CERT_CN=<the extracted Common Name of implant.pem>

Constraints:
- You must use standard Linux CLI tools (grep, awk, base64, find, openssl, etc.).
- Ensure `/home/user/report.txt` contains no extra spaces around the equals signs.