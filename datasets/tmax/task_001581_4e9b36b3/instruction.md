You are a DevSecOps engineer responsible for enforcing policy as code and securing legacy applications. We have a stripped legacy web server binary located at `/home/user/legacy_server`. It is known to contain a hidden, undocumented administrative endpoint that sets an insecure cookie and lacks a Content Security Policy (CSP).

Your task is to analyze the binary, securely interact with it, and document your findings. 

Perform the following steps:
1. Reverse engineer the binary `/home/user/legacy_server` to discover the hidden HTTP GET endpoint path. (Hint: look for strings resembling API paths).
2. Write a Bash script at `/home/user/audit_server.sh` that does the following:
   - Uses process isolation by setting a strict virtual memory limit of 50,000 KB (`ulimit -v 50000`) for the current shell.
   - Starts the `/home/user/legacy_server` binary in the background (it listens on port 8888 by default).
   - Waits up to 2 seconds for the server to start.
   - Uses `curl` to send a GET request to the hidden administrative endpoint you discovered.
   - Inspects the HTTP response headers to extract the name of the session cookie being set by the `Set-Cookie` header (only the cookie name, not the value).
   - Gracefully terminates the background server process.
3. The script must then output a final report to `/home/user/audit_results.txt` with exactly the following format (replace the bracketed placeholders with your findings):
```
Endpoint: [Hidden_Path]
Cookie: [Cookie_Name]
CSP: Content-Security-Policy: default-src 'self'; script-src 'self';
```

Constraints:
- You must use Bash for your script.
- The CSP provided in the report must strictly enforce `default-src 'self'` and `script-src 'self'` exactly as formatted above.
- Make sure your bash script `/home/user/audit_server.sh` is executable and runs successfully to generate the file.