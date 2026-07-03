You are a compliance analyst responsible for generating secure audit trails for an application's authentication flows. Recently, security audits revealed that raw authentication logs contained plaintext credentials, exploit payloads (like XSS or SQLi attempts), and lacked proper Content Security Policy (CSP) validations.

Your task is to write a Python script at `/home/user/audit_filter.py` that acts as a log sanitiser and compliance detector. 

Additionally, the exact redaction "salt" required by corporate policy is stored in an old scanned memo located at `/app/policy_memo.png`. You must use optical character recognition (OCR) within your script to read this image and extract the salt. Tesseract and the `pytesseract` Python library are pre-installed. The image contains a line formatted exactly as `MANDATORY REDACTION SALT: <SALT_VALUE>`. 

Your script must conform to the following CLI usage:
`python3 /home/user/audit_filter.py <input_json_file> <output_json_file>`

Each input JSON file represents a single HTTP request/response log entry. Example structure:
```json
{
  "endpoint": "/api/v1/login",
  "method": "POST",
  "headers": {
    "User-Agent": "Mozilla/5.0",
    "Content-Security-Policy": "default-src 'self'"
  },
  "payload": {
    "username": "admin",
    "password": "my_plaintext_password"
  }
}
```

Your script must parse the input JSON and apply the following compliance rules to write to the output JSON:
1. **Sensitive Data Redaction (Auth Flow):** If the `payload` dictionary contains a `password` key, and its value is a plaintext string (defined as NOT being a 64-character lowercase hex string, which would indicate a SHA-256 hash), you must replace the password's value with the string `[REDACTED: <SALT_VALUE>]` (where `<SALT_VALUE>` is the exact string extracted from the image).
2. **Exploit Delivery Detection:** If any string value within the `payload` or `headers` dictionaries contains the substring `<script>` (case-insensitive) or `${jndi:` (case-insensitive), replace that specific string value entirely with `[EXPLOIT_BLOCKED]`.
3. **CSP Enforcement:** If the `headers` dictionary does NOT contain a `Content-Security-Policy` key, or if the CSP string does not contain the substring `default-src 'self'`, you must inject a new top-level key into the JSON object: `"COMPLIANCE_WARNING": "MISSING_CSP"`.

If an input log violates NONE of these rules (i.e., it is a clean, compliant authentication log with hashed passwords, no exploits, and valid CSP), your script MUST write the exact original JSON structure to the output file without any modifications.

Requirements:
- Output valid JSON.
- Process all string fields defensively.
- Do not modify clean files in any way (they should be semantically identical).