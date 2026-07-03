You are a compliance analyst generating an automated audit trail for a newly deployed internal web service. The developers have deployed a mock version of their service locally on a random port between 8000 and 9000 on `127.0.0.1`.

Your task is to write a Python script at `/home/user/audit_service.py` that programmatically audits this service and generates an audit report. You may use shell tools to investigate before writing your script, but the final audit generation must be handled by your Python script.

The Python script must perform the following actions:
1. **Service Discovery:** Discover the exact port the HTTPS service is running on.
2. **Certificate Validation:** Connect to the service via HTTPS and extract the Subject of the SSL certificate.
3. **Content Security Policy Auditing:** Fetch the HTTP headers from the root endpoint (`/`) and parse the `Content-Security-Policy` header. You need to determine if the `script-src` directive contains the strongly discouraged `'unsafe-inline'` policy.
4. **Exploit Verification:** If the CSP contains `'unsafe-inline'`, the service might be vulnerable to Cross-Site Scripting (XSS). The developers created an endpoint `/submit?q=<input>` for testing. Craft an XSS payload containing the exact string `<script>alert(1)</script>` and deliver it via a GET request to the `q` parameter of the `/submit` endpoint. Check if the server returns an HTTP 200 response and reflects your payload in the response body.

Your script must generate a JSON-formatted audit trail saved exactly at `/home/user/audit_report.json` with the following structure:

```json
{
  "service_port": <integer, the port number>,
  "cert_subject": "<string, the raw string representation of the certificate Subject (e.g., as returned by Python's ssl module or OpenSSL)>",
  "csp_unsafe_inline": <boolean, true if 'unsafe-inline' is present in script-src>,
  "exploit_successful": <boolean, true if the payload was successfully reflected with a 200 OK>
}
```

Constraints:
- You are not allowed to use external third-party Python libraries like `requests` (use standard libraries like `http.client`, `urllib`, `ssl`, `socket`, or call standard shell tools using `subprocess`).
- Ignore SSL certificate validation errors (the service uses a self-signed certificate for local testing).
- The final verification will only check `/home/user/audit_report.json`.