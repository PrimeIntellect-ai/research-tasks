You are a security auditor tasked with evaluating a local Python web application. A developer has deployed a prototype service on this machine, but we suspect it has multiple security vulnerabilities, including credential leakage, insecure HTTP headers, and embedded secrets in compiled code. 

Your objective is to audit the running environment, interact with the service, and extract the required security flags. You must use standard Bash command-line tools (shell built-ins, coreutils, curl, strings, etc.) to complete this task.

Perform the following steps:
1. **Service Auditing & Credential Leakage:** Discover the custom Python web service running on localhost. The service is launched by a script that insecurely passes an administrative authentication token as a command-line argument. Find this leaked token by inspecting process information.
2. **HTTP Header & Cookie Inspection:** Use the leaked token to authenticate against the web service. You must pass the token in a cookie named `auth_token`. When making an authenticated GET request to the root endpoint (`/`), inspect the HTTP response headers. Identify the custom header starting with `X-Missing-` which indicates a missing security policy (e.g., a missing Content-Security-Policy). Also, download the file referenced in the response body.
3. **Reverse Engineering:** The authenticated response body contains a URL path to download a compiled Python file (`/download/module.pyc`). Download this file using your authenticated session. Reverse engineer or extract strings from this compiled Python file to find a hidden flag in the format `FLAG{...}`.

Finally, write your findings to a file exactly at `/home/user/audit_report.txt` with the following strict format:
Line 1: The port number the web service is running on.
Line 2: The exact leaked authentication token.
Line 3: The name of the missing security header identified (e.g., `X-Missing-Policy`).
Line 4: The hidden flag extracted from the compiled Python file.

Example `/home/user/audit_report.txt` format:
8080
secret_token_123
X-Missing-CSP
FLAG{example_flag}