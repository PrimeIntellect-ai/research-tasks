You are a red-team operator simulating an attack against a web application protected by a custom Web Application Firewall (WAF). Your goal is to craft a specific XSS payload that can bypass the WAF's filters.

You have been provided with an access log from previous automated evasion attempts located at `/home/user/access.log`. The WAF inspects the `Cookie: session=` header for malicious payloads. When the WAF detects a payload, it blocks the request and returns an HTTP 403 status code. If the payload bypasses the filter, the application processes it and returns an HTTP 200 status code.

Your tasks are to:
1. Analyze `/home/user/access.log` to identify the single HTTP request that successfully bypassed the WAF (HTTP 200).
2. Extract the encoded payload from the `session=` cookie of that successful request.
3. Analyze the successful payload to determine the exact encoding sequence used. The original payload for all attempts in the log was `<script>alert(1)</script>` or similar simple XSS vectors, but the successful one used a custom combination of string manipulation and standard encoding to evade the WAF.
4. Once you have deduced the exact two-step encoding mechanism, apply the identical encoding sequence to the following new XSS payload:
   `<svg onload=alert(document.domain)>`
5. Save your final encoded payload string to `/home/user/payload.txt`. The file should contain only the encoded string and absolutely no trailing newlines or other text.

Ensure you use Bash and standard Linux command-line utilities to perform your analysis and craft the payload.