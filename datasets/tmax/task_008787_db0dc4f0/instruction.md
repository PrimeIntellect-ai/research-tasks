You are an incident responder investigating a recent security breach on a web application. The application is written in Go. Several users have reported that their session tokens were stolen, and we suspect a Reflected Cross-Site Scripting (XSS) vulnerability was used in conjunction with insecure cookie configurations.

You have been provided with the source code of the vulnerable application at `/home/user/server.go` and the web server access logs at `/home/user/access.log`.

Your objectives are to secure the application code and identify the attackers from the logs.

1. **Fix the Go Web Server**
Analyze `/home/user/server.go`. You need to address the following issues and save the corrected code to `/home/user/server_fixed.go`:
- **XSS Vulnerability:** The `/greet` endpoint takes a `name` query parameter and reflects it directly into the HTML response. Fix this by escaping the input using the standard `html.EscapeString` function before writing it.
- **Insecure Cookies:** The server sets a `session_token` cookie, but it lacks security attributes. Modify the cookie creation so that both `HttpOnly` and `Secure` flags are set to `true`.
- **Content Security Policy:** To prevent future injection attacks, enforce a strict CSP. Add the HTTP header `Content-Security-Policy` with the exact value `default-src 'self'` to the responses in the `/greet` handler.

2. **Log Analysis via Bash**
We need to know which IP addresses successfully exploited the XSS vulnerability. 
Write a bash script at `/home/user/analyze.sh` that parses `/home/user/access.log`. 
The script must:
- Find all log entries where the HTTP request line contains the URL-encoded script tag `%3Cscript%3E` (case-insensitive).
- Ensure the server responded with a HTTP `200` status code for that request.
- Extract the IP addresses (the first space-separated field in the log) of these successful attacks.
- Save the unique IP addresses, sorted in standard ascending order, to `/home/user/compromised_ips.txt` (one IP per line).

Ensure `/home/user/analyze.sh` is executable and run it so the `compromised_ips.txt` file is generated.