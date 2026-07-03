You are a security engineer tasked with rotating credentials and securing a legacy login service. The legacy service is provided as a compiled, stripped binary located at `/app/auth_service`. You do not have the source code, but you know it listens on `127.0.0.1:8080` when executed.

Security audits have revealed several vulnerabilities in `/app/auth_service`:
1. It is susceptible to an open redirect vulnerability (it will redirect users to absolute external URLs provided in a query parameter).
2. It fails to set Content Security Policy (CSP) headers.
3. It issues session cookies without the `HttpOnly` and `Secure` flags.
4. It is vulnerable to an exploit from a known malicious scanner, which always sends the HTTP header `X-Block-Me: true`.

Your task is to write an application-level firewall and reverse proxy entirely in Bash to mitigate these issues, without modifying the binary itself.

1. Create a Bash script at `/home/user/proxy_worker.sh`. Ensure it is executable.
2. This script will be invoked for every incoming HTTP connection using `socat`. For example, a user might run:
   `socat TCP-LISTEN:9000,reuseaddr,fork EXEC:/home/user/proxy_worker.sh`
3. Your script must read the incoming HTTP request from standard input (stdin) and process it as follows:
   - **Firewall Rule:** Inspect the request headers. If the header `X-Block-Me: true` is present, immediately output a valid HTTP `403 Forbidden` response (including proper HTTP response line and blank line before body) and exit, dropping the request.
   - **Proxy:** If the request is allowed, forward the raw HTTP request to the backend service at `127.0.0.1:8080` (you can use `nc` or bash `/dev/tcp` for this).
   - **CSP Enforcement:** Inject the header `Content-Security-Policy: default-src 'self'` into the HTTP response returned by the backend.
   - **Open Redirect Mitigation:** Inspect the `Location` response header. If it contains an absolute URL (starting with `http://` or `https://`), rewrite it to `Location: /error`. Relative redirects (like `Location: /dashboard`) must be left intact.
   - **Cookie Inspection:** Inspect any `Set-Cookie` response headers. Append `; HttpOnly; Secure` to the cookie value if it is not already present.
4. Output the fully reconstructed, secured HTTP response to standard output (stdout) so `socat` can send it back to the client.

To test your implementation, start the binary `/app/auth_service` in the background, set up your `socat` listener on port 9000, and ensure your Bash script successfully processes and sanitizes requests. The automated verification will test your proxy using a suite of valid and malicious requests.