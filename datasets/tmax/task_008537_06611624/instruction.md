You are a DevSecOps engineer implementing a policy-as-code check for an incoming webhook gateway. You need to write a Bash script that analyzes a batch of recorded HTTP requests, verifies their authentication tokens, and inspects their payloads for malicious patterns.

Write a Bash script at `/home/user/analyze_requests.sh` that performs the following steps:

1. Iterate over all `.b64` files in the directory `/home/user/incoming_requests/`. Each file contains a Base64-encoded raw HTTP request.
2. Decode each file's contents to inspect the raw HTTP request.
3. **Authentication Flow Testing**: Extract the token from the `Authorization: Bearer <token>` header. A valid token must consist of exactly 16 lowercase hexadecimal characters (e.g., `a1b2c3d4e5f60789`). If the token is missing or does not match this exact format, the authentication status is `AUTH_FAIL`. Otherwise, it is `AUTH_OK`.
4. **Intrusion Detection (Pattern Matching)**: Extract the HTTP request body (everything after the first empty line). Check if the body contains any of the exact strings listed in `/home/user/signatures.txt`. If any of the signatures are found in the body, the threat status is `THREAT_DETECTED`. Otherwise, it is `CLEAN`.
5. **Logging**: Append the results for each file to `/home/user/audit_log.csv` in the exact format:
   `filename,auth_status,threat_status`
   (Sort the output alphabetically by filename so it is consistent. Only output the base filename, e.g., `req1.b64`).

Execute your script so that `/home/user/audit_log.csv` is generated successfully. Ensure your script is executable (`chmod +x`). 

Assume the directory `/home/user/incoming_requests/` and the file `/home/user/signatures.txt` already exist and are populated.