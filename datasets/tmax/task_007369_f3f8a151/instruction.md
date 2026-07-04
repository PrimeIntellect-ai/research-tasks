You are an incident responder investigating a custom web server written in C. We have identified several security vulnerabilities in the server's code. The server's source code is located at `/home/user/server.c`. 

Your task is to audit the code, implement several security fixes, compile the server, and run it in the background.

Perform the following modifications to `/home/user/server.c`:

1. **Sensitive Data Redaction**: The server currently logs the raw request paths to `/home/user/access.log`. Modify the logging logic so that if a request path contains the parameter `token=`, its value is redacted in the log file. Replace the token's value with the exact string `REDACTED`. The token value consists of characters up to the next `&` or the end of the string.
   - Example original: `/api?user=1&token=secret123&action=view`
   - Example logged: `/api?user=1&token=REDACTED&action=view`

2. **Open Redirect Mitigation**: The server has a `/login?redirect=` endpoint that is vulnerable to open redirects. Modify the logic so that it only permits redirects to paths that begin exactly with `/dashboard` or `/profile`. If the provided redirect parameter does not start with one of these two strings, force the redirect location to `/dashboard`.

3. **Content Security Policy Enforcement**: The server's 200 OK response does not enforce a Content Security Policy. Add the following HTTP response header to the 200 OK response:
   `Content-Security-Policy: default-src 'self';`

Once you have made the necessary code changes:
4. Compile the updated server using `gcc /home/user/server.c -o /home/user/server`.
5. Run the compiled server executable `/home/user/server` in the background (it is configured to listen on port 8080). Do not change the port.

You may use standard C library functions (e.g., `strstr`, `strncmp`, `snprintf`) to implement these changes.