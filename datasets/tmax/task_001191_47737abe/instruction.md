You are a compliance analyst tasked with generating an automated security audit trail. A recent incident requires you to correlate network-level access logs with application-level authentication logs to identify successful login sessions and suspicious IPs performing brute-force attacks.

You have been provided with two log files:
1. `/home/user/access.log` - The frontend web server log containing network details and HTTP headers.
2. `/home/user/app.log` - The backend authentication service log containing authentication events.

Your task is to write and execute a Python script that correlates the entries in both files using the Correlation ID and generates a JSON audit report.

**Details & Requirements:**

1. **Log Correlation:**
   - Both logs contain a Correlation ID. 
   - In `access.log`, it is found in the JSON-formatted Headers field as `X-Correlation-ID`.
   - In `app.log`, it is enclosed in brackets, e.g., `[CorrID: C001]`.

2. **HTTP Cookie Inspection (Successful Logins):**
   - For every `LOGIN_SUCCESS` event in `app.log`, find the corresponding request in `access.log`.
   - Extract the value of the `session_id` cookie from the `Cookie` header. Keep only the value of `session_id` (ignore other cookies in the string).

3. **Authentication Flow Testing (Suspicious IPs):**
   - For every `LOGIN_FAILED` event in `app.log`, find the originating IP address in the corresponding `access.log` entry.
   - Count the number of failed login attempts per IP address.
   - Any IP address with strictly more than 2 failed attempts should be flagged as suspicious.

4. **Output Format:**
   - Write your final results to a JSON file at `/home/user/audit_report.json`.
   - The JSON file must have exactly this structure:
     ```json
     {
       "successful_sessions": [
         "extracted_session_id_1",
         "extracted_session_id_2"
       ],
       "suspicious_ips": [
         "192.168.1.100"
       ]
     }
     ```
   - Sort the arrays in the JSON output alphabetically to ensure consistent automated testing.

Write a Python script, run it to generate the report, and ensure the output file is saved precisely at `/home/user/audit_report.json`.