You are a compliance analyst tasked with generating secure audit trails from raw web access logs and extracting malicious IPs for our firewall rules. 

You have been provided with raw access logs in JSONL format at `/home/user/raw_logs.jsonl`. Each line contains an access event with an `ip`, an `endpoint`, and a JWT `token` used for authorization.

Additionally, our infrastructure's public certificates are located in `/home/user/certs/`. This directory contains a root CA certificate (`ca.crt`) and the API server's certificate (`server.crt`).

Your task is to write and execute a Go program at `/home/user/process_audit.go` that performs the following steps:
1. **Certificate Validation**: Load `ca.crt` and `server.crt`. Use Go's `crypto/x509` package to verify that `server.crt` is valid and signed by `ca.crt`. Extract the RSA public key from `server.crt`.
2. **Log Processing**: Read the `raw_logs.jsonl` file line by line.
3. **Token Validation**: For each log entry, parse and validate the JWT `token` using the extracted RSA public key. You should use the `github.com/golang-jwt/jwt/v5` module for this.
4. **Network Policy Extraction**: If a token is *invalid* (e.g., signature mismatch, expired), extract the `ip` address and append it to `/home/user/blocklist.txt` (one IP per line).
5. **Data Redaction & Audit Trail**: If a token is *valid*, write the log entry to `/home/user/audit_trail.jsonl` (as a JSONL file) but strictly redact the token by replacing its value with the exact string `"REDACTED"`. Keep the `ip` and `endpoint` fields intact.

**Requirements**:
- Initialize your Go module in `/home/user/` and fetch the required JWT library before running your code.
- Your Go code should correctly handle standard JSON serialization and deserialization.
- The `blocklist.txt` file must only contain the IPs of failed validations.
- The `audit_trail.jsonl` file must contain valid JSON lines for successful validations.

Complete the task by ensuring both `/home/user/blocklist.txt` and `/home/user/audit_trail.jsonl` are correctly generated.