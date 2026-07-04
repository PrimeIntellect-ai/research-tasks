You are a network engineer inspecting secure traffic logs for a legacy system. You have been given an encrypted traffic capture and a custom C utility used to decrypt and inspect the traffic. However, the utility is currently broken, contains a severe security vulnerability, and is missing its cryptographic environment.

Your objective is to set up the environment, audit and fix the utility, and extract the decrypted traffic.

Here are your specific tasks:

1. **TLS Certificate Management:**
   The backend system requires a self-signed certificate to function (simulated in this environment).
   - Create a directory `/home/user/certs/`.
   - Generate a new RSA 2048-bit private key at `/home/user/certs/server.key`.
   - Generate a self-signed X.509 certificate at `/home/user/certs/server.crt` valid for 365 days. The Common Name (CN) must be exactly `inspector.local`.

2. **Code Audit and CWE Remediation:**
   The inspection utility is located at `/home/user/inspector/traffic_inspector.c`.
   - Analyze the C code. There is a classic CWE-120/CWE-121 (Buffer Overflow) vulnerability in the `parse_request` function which crashes the program when processing large headers.
   - Fix the vulnerability in `traffic_inspector.c` to ensure it safely handles arbitrary-length request strings without overflowing the stack buffer.

3. **Content Security Policy Injection:**
   The utility is supposed to inject a security header into the decrypted HTTP output, but the implementation is missing.
   - Modify `traffic_inspector.c` so that immediately after it prints the decrypted HTTP status line (e.g., `HTTP/1.1 200 OK`), it inserts the following exact header on a new line:
     `Content-Security-Policy: default-src 'self';`

4. **Compile and Execute:**
   - Compile the fixed utility: `gcc /home/user/inspector/traffic_inspector.c -o /home/user/inspector/traffic_inspector -lcrypto`
   - Run the utility. It reads the encrypted payload from `/home/user/inspector/traffic.enc` and the 256-bit AES key from `/home/user/inspector/key.bin`.
   - The utility will automatically write the output to `/home/user/inspector/decrypted_log.txt` if it doesn't crash.

Verify that `/home/user/inspector/decrypted_log.txt` exists, contains the successfully decrypted HTTP response, and includes the injected CSP header correctly.