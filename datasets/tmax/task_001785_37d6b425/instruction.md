You are a security auditor assigned to evaluate an internal report generation service and verify proper handling of sensitive permission data.

An internal Flask web application is located at `/home/user/app/server.py`. It is currently not running. Your task involves auditing this application, exploiting a vulnerability to extract restricted data, and securely processing that data.

Perform the following steps:
1. Start the Flask application. It binds to `127.0.0.1:5000`. You may need to install Flask if it's not present.
2. The application has an endpoint `/generate` that accepts POST requests with a form field named `template`. Analyze `server.py` to identify a Server-Side Template Injection (SSTI) vulnerability.
3. Craft an exploit payload to read the contents of the restricted file `/home/user/secret_permissions.json` through the `/generate` endpoint. Do not read the file directly from the filesystem—you must prove the vulnerability exists by extracting it through the web application.
4. Write a Python script at `/home/user/process_audit.py` that takes the extracted JSON data and performs sensitive data redaction. Specifically, the script must parse the JSON and replace the values of any keys named exactly `ssn` or `password` with the literal string `***`.
5. The script must save the redacted JSON to `/home/user/redacted_report.json`. The JSON must be formatted with an indentation of 4 spaces and have its keys sorted alphabetically (i.e., `json.dump(..., indent=4, sort_keys=True)`).
6. Calculate the SHA-256 cryptographic hash of the exact contents of the resulting `/home/user/redacted_report.json` file. Save this hash (as a lowercase hex string) to `/home/user/report_hash.txt`.

Your final deliverables must include:
- `/home/user/process_audit.py`
- `/home/user/redacted_report.json` (extracted via exploit, then redacted and formatted)
- `/home/user/report_hash.txt` (containing only the sha256 hex digest of the redacted JSON file)