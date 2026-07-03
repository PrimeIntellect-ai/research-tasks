You are a DevSecOps engineer responding to a security incident. We suspect our authentication service has been exploited using a JWT "alg: none" bypass vulnerability. You need to analyze the logs, redact sensitive information, extract the attackers' IPs, and generate a network policy to block them.

You have been provided with an application log file at `/home/user/auth_logs.txt`. 
The log file contains entries in the following format:
`[TIMESTAMP] | IP_ADDRESS | HTTP_STATUS | JWT_TOKEN`

Your task is to:
1. Write a Go program at `/home/user/secops.go` to process the log file.
2. **Log Parsing & Correlation:** The Go program must parse the logs and identify malicious IP addresses. An IP is considered malicious if it made a request with a `HTTP_STATUS` of `200` AND the provided `JWT_TOKEN` exploits the bypass. To check this, base64-decode the header (the first part of the JWT, before the first dot). If the decoded JSON header contains `"alg":"none"` (ignoring whitespace variations), it is an exploit payload.
3. **Data Redaction:** The Go program must also redact all JWT tokens from the log file to prevent credential leakage. Replace the entire JWT string (header.payload.signature) with the exact string `[REDACTED_JWT]`. Write the cleaned logs to `/home/user/clean_auth_logs.txt`, maintaining the exact original spacing and format otherwise.
4. **Network Policy Configuration:** After running your Go program to identify the malicious IPs, create a Kubernetes NetworkPolicy file at `/home/user/deny_policy.yaml` to block *only* the identified malicious IPs from accessing the pods with the label `app: auth-service`. The policy should use an `ipBlock` with `cidr: 0.0.0.0/0` and place the malicious IPs (formatted as `<IP>/32`) in the `except` array. Sort the IPs in the `except` array in ascending alphabetical order.
5. **Checksum Verification:** Finally, compute the SHA256 checksum of `/home/user/clean_auth_logs.txt` and save it to `/home/user/checksum.txt` in the standard `sha256sum` format (e.g., `<hash>  /home/user/clean_auth_logs.txt`).

Ensure all files are created in `/home/user/` and have the exact names specified.