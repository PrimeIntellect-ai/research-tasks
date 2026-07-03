You are an incident responder investigating a recent phishing campaign that exploited an Open Redirect vulnerability (CWE-601) in a custom C-based HTTP response generator used by our login portal.

Your environment is set up in `/home/user/incident`. Inside this directory, you will find:
1. `auth_server.c`: A C program that takes a simulated query string as a command-line argument and prints an HTTP 302 response to stdout.
2. `sshd_config`: A backup of the compromised server's SSH daemon configuration.

Your objectives are:

1. **Code Auditing & Patching (CWE-601 & CSP Enforcement):**
   - Audit `/home/user/incident/auth_server.c` and fix the Open Redirect vulnerability. Currently, it directly reflects the `redirect_to=` parameter into the `Location` header.
   - Modify the logic so that if the redirect target starts with `http://`, `https://`, or `//`, it must instead redirect to exactly `/error`. Otherwise, it should redirect to the provided path.
   - Enhance the security by adding a Content Security Policy header to the HTTP response. Specifically, add exactly: `Content-Security-Policy: default-src 'self';` on its own line before the blank `\r\n` that ends the headers.
   - Compile the fixed program to `/home/user/incident/auth_server` using `gcc`.

2. **TLS/SSL Certificate Management:**
   - The web team is moving the server to HTTPS. Generate a self-signed RSA 2048-bit TLS certificate and private key.
   - Place them at `/home/user/incident/cert.pem` and `/home/user/incident/key.pem`.
   - The certificate must be valid for 365 days and have the Common Name (CN) set to `localhost`. Do not encrypt the private key.

3. **SSH Hardening:**
   - Audit `/home/user/incident/sshd_config`.
   - Update the configuration to securely prevent unauthorized access: Set `PermitRootLogin` to `no` and `PasswordAuthentication` to `no`. Leave other existing settings intact.

4. **Testing & Verification:**
   - Create a bash script at `/home/user/incident/test.sh` that runs the compiled `/home/user/incident/auth_server` twice.
   - First run argument: `redirect_to=http://evil.com`
   - Second run argument: `redirect_to=/dashboard`
   - The script must append the stdout of both runs to `/home/user/incident/test_output.log`.
   - Run the script so the log file is generated.