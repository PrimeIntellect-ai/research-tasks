You are acting as a compliance analyst for a financial organization. We are setting up a secure audit logging pipeline that receives vulnerability scan results and verifies their integrity before writing them to the final audit trail.

Your task consists of two parts: Infrastructure Configuration and Log Integrity Processing.

**Part 1: Secure Audit Pipeline Infrastructure**
We have a local log receiver backend (a Flask application) running on port 5000. It is located at `/app/receiver.py`.
You must set up an Nginx reverse proxy to secure this service. 
1. Generate a self-signed RSA-2048 TLS certificate and private key. Place them in `/home/user/certs/tls.crt` and `/home/user/certs/tls.key`.
2. Create an Nginx configuration file at `/home/user/nginx.conf` that listens on port 8443 (HTTPS) using your generated certificates, and proxies all requests to `http://127.0.0.1:5000`.
3. Start the Nginx service using your configuration (e.g., `nginx -c /home/user/nginx.conf`).

**Part 2: Audit Log Integrity Verification**
The vulnerability scanner sends raw log lines to the pipeline. Because logs traverse untrusted zones, each log message is appended with an HMAC-SHA256 signature.
You must write a Python script at `/home/user/log_normalizer.py` that reads lines from standard input and prints the verified output to standard output.

Input Format:
Each line from standard input will be in the format:
`<HMAC_HEX>:<RAW_MESSAGE>`

The `<HMAC_HEX>` is the hex-encoded HMAC-SHA256 signature of the `<RAW_MESSAGE>`.
The secret key used for the HMAC is the string `COMPLIANCE_KEY_2024`.

Output Format:
For each line of input:
- If the HMAC matches the message, output: `[VERIFIED] <RAW_MESSAGE>`
- If the HMAC does NOT match, output: `[TAMPERED] <RAW_MESSAGE>`

Your script must process all lines from standard input until EOF and match the output format exactly.

Ensure that the Nginx service is running and accessible on port 8443, and your `log_normalizer.py` script is fully implemented and executable.