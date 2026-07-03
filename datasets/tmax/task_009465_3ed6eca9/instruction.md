You are acting as a penetration tester analyzing an offline capture of a web application's configuration and traffic. You have been provided with an audit directory at `/home/user/api_audit` containing two files:
1. `server.crt`: The public SSL/TLS certificate of the web server.
2. `traffic.log`: A capture of raw HTTP requests sent to the server.

Your objective is to analyze these files to identify a staging environment, extract leaked credentials, and forge an authentication token to demonstrate the vulnerability.

Follow these exact steps:

1. **Certificate Inspection**: Analyze the `server.crt` file. Look at the Subject Alternative Name (SAN) extension. There is one DNS name that contains the word "staging". Identify this exact staging hostname.
2. **Traffic Analysis**: Inspect `traffic.log` for an HTTP request directed to the staging hostname you just identified (check the `Host` header). In this specific request, the developers accidentally left a debug header `X-Debug-Secret` which contains the signing secret for the API tokens. Extract this secret.
3. **Token Analysis & Forgery**: 
   - Observe the `Cookie` header in that same staging request. The `session_auth` cookie is a Base64-encoded string.
   - When decoded, the token format is: `username|timestamp|signature`
   - The `signature` is an MD5 hash of the string: `username|timestamp|secret` (using the secret you found).
   - You must forge a new token for the user `admin` with the fixed timestamp `1800000000`.
   - Calculate the new MD5 signature, construct the full string, and Base64-encode it to create the new `session_auth` cookie.

Write your final findings to a file exactly at `/home/user/report.txt` with the following format:
Line 1: The staging hostname (e.g., `staging.example.com`)
Line 2: The extracted secret from the HTTP header
Line 3: The fully forged, Base64-encoded `session_auth` cookie for the admin user

Do not include any extra spaces or text on these lines.