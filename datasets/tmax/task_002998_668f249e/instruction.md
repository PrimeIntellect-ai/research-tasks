You are a network security engineer investigating a legacy authentication system that has been intercepted. The system is vulnerable to an open redirect attack during its login flow and uses a proprietary, weak cryptographic algorithm for session tokens. 

Your objective is to build a secure proxy service in C++ that intercepts login requests, decrypts the tokens to recover the original passwords, mitigates the open redirect vulnerability, and injects proper Content Security Policy (CSP) headers.

We have extracted the proprietary token generation utility from the legacy server. It is available as a stripped binary at `/app/legacy_crypto`. 
- The binary takes a 4-character ASCII password as a command-line argument and outputs a hex-encoded token.
- You must analyze (reverse-engineer or black-box brute-force) this binary to understand the weak cipher it uses, as you will need to implement a cracking/decryption function in your C++ proxy.

Your task is to write and run a C++ HTTP server listening on `127.0.0.1:8080`. 

The server must implement the following specification:
1. Accept HTTP `POST` requests to the endpoint `/login`.
2. Parse `application/x-www-form-urlencoded` request bodies containing two parameters: `token` and `redirect`.
3. **Cryptanalysis & Cracking:** Decrypt the hex `token` to recover the original 4-character password. Implement this decryption logic in your C++ code.
4. **Open Redirect Mitigation:** Validate the `redirect` parameter. The server should only allow local relative redirects (e.g., paths starting with a single `/`, like `/dashboard`). If the redirect URL is absolute (contains `http://`, `https://`, or starts with `//`), the server must reject the request by returning an HTTP 400 Bad Request.
5. **CSP Enforcement:** For successful requests, return an HTTP 200 OK. The response MUST include the header: `Content-Security-Policy: default-src 'self';`.
6. **Response Body:** The body of a successful 200 OK response must be exactly the recovered 4-character plaintext password.

Requirements:
- Your proxy must be written in C++ (`g++` is available to compile it).
- You may use standard POSIX sockets (`<sys/socket.h>`) to implement the HTTP server. You do not need a full-fledged HTTP library, just enough to parse the POST body, validate the redirect, and send the correct HTTP response headers and body.
- Leave the server running in the background once compiled and started so it can be verified.