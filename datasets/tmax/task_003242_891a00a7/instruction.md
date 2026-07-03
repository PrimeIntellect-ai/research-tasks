You are acting as a compliance analyst. We have captured a batch of API access logs from our internal gateway. Security has alerted us that one of our microservices might be vulnerable to a JWT "algorithm=none" bypass attack, where malicious actors can forge tokens by setting the signature algorithm to "none" (or "None", "NONE", etc.) and dropping the signature.

Your task is to write a Python script to automatically scan these logs, decode the JWT payloads, detect any intrusion attempts exploiting this vulnerability, and generate an audit trail of the compromised access attempts.

Here are the details:

1. **Input File:** You will find the logs at `/home/user/api_logs.jsonl`. Each line is a JSON object representing an HTTP request, containing keys such as `timestamp`, `ip_address`, `endpoint`, and `auth_header`.
2. **JWT Format:** The `auth_header` usually contains a string like `Bearer <token>`. A JWT consists of three Base64Url-encoded parts separated by dots: `Header.Payload.Signature`.
3. **Detection Logic:** 
   - Extract the JWT from the `auth_header`.
   - Base64Url-decode the **Header** and parse it as JSON. (Remember to handle missing Base64 padding, as JWTs omit standard padding).
   - Check if the `"alg"` key in the Header is set to `"none"` (case-insensitive).
   - If it is, this is a confirmed exploit attempt. Base64Url-decode the **Payload** and parse it as JSON.
4. **Audit Trail Generation:** 
   - For every detected exploit attempt, extract the `"user_id"` from the decoded JWT Payload, along with the `ip_address` and `timestamp` from the original log line.
   - Write the findings to `/home/user/audit_trail.csv`.
   - The CSV must have the exact header: `timestamp,ip_address,user_id`.
   - Write the records in the order they appear in the log file.

You must only use standard Python libraries (e.g., `json`, `base64`, `csv`). External libraries like `PyJWT` are not available and should not be used. Write and execute the script to generate `/home/user/audit_trail.csv`.