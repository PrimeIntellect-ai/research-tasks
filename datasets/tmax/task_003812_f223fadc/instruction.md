You are a network security engineer tasked with auditing and fixing a prototype Rust-based network traffic inspection tool. The tool is designed to securely fetch sensitive data from an internal server, but the previous developer took some dangerous shortcuts.

The source code is located at `/home/user/traffic-auditor/src/main.rs`. 

Currently, the tool has two major security flaws:
1. **CWE-295 (Improper Certificate Validation):** The HTTPS client is currently configured to accept any invalid or self-signed certificate.
2. **CWE-732 (Incorrect Permission Assignment):** The program writes sensitive intercepted data to a file without restricting file permissions, leaving it readable by any user on the system.

There is a local HTTPS server running on `https://127.0.0.1:8443/secure-endpoint`. 

Your task is to fix the code and execute the pipeline:
1. Audit and modify `/home/user/traffic-auditor/src/main.rs`. Remove the insecure certificate bypass.
2. Configure the HTTP client to properly validate the certificate chain using the Root CA certificate located at `/home/user/ca.crt`.
3. The tool must make a GET request to `https://127.0.0.1:8443/secure-endpoint`.
4. Inspect the HTTP response headers and extract the value of the `session_token` cookie (e.g., if the header is `Set-Cookie: session_token=XYZ123; Secure`, extract `XYZ123`).
5. Compute the SHA-256 hash of this extracted cookie value.
6. Write the resulting lowercase hexadecimal SHA-256 hash string to exactly `/home/user/cookie_hash.txt`.
7. Fix the file permission flaw: Ensure that the Rust program creates or modifies `/home/user/cookie_hash.txt` so it ends up with strict `0600` (rw-------) permissions. 
8. Compile and run your fixed Rust program so the output file is generated correctly.