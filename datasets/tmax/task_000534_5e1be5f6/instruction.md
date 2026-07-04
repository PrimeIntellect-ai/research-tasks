You are a compliance analyst tasked with generating an encrypted audit trail of a vulnerability in an internal C++ authentication service, and then securing the application.

A custom-built authentication service runs locally on port `8080`. The source code is located at `/home/user/auth_service.cpp`. 
Currently, the service processes login requests and takes a `redirect` parameter. However, it is vulnerable to Server-Side Request Forgery (SSRF) and Local File Inclusion because it fetches and returns the contents of the URL/URI provided in the `redirect` parameter without proper validation.

Your tasks are to:

1. **Exploit the Vulnerability (Audit Trail Generation):**
   Use `curl` or a similar tool to exploit the running service on `http://127.0.0.1:8080/login` to read the contents of the highly sensitive file located at `/home/user/vault/secret.key`.
   Save the exact response (the leaked secret) into a file named `/home/user/evidence.txt`.

2. **Develop a C++ Encryption Tool:**
   To safely store this audit evidence, you must write a C++ program at `/home/user/crypto_tool.cpp` that reads `/home/user/evidence.txt`, encrypts it using a repeating-key XOR cipher, and writes the output to `/home/user/evidence.enc`.
   - The XOR key must be the string: `COMPLIANCE_KEY_2024`
   - The C++ program should take the input file path, output file path, and key string as command-line arguments (e.g., `./crypto_tool /home/user/evidence.txt /home/user/evidence.enc COMPLIANCE_KEY_2024`).
   - Compile your code to `/home/user/crypto_tool` and run it to generate the `/home/user/evidence.enc` file.

3. **Remediate the Vulnerability (Secure Coding):**
   Create a patched version of the server source code at `/home/user/auth_service_fixed.cpp`. 
   Implement an input validation mechanism that ensures the `redirect` parameter ONLY accepts URLs starting exactly with `http://internal.company.local/`. If any other scheme (like `file://` or `http://evil.com/`) is provided, the service should return the string `HTTP/1.1 403 Forbidden\r\n\r\nInvalid redirect` instead of fetching the resource.
   Compile this fixed version to `/home/user/auth_service_fixed`.

Make sure all created files exactly match the paths and names specified.