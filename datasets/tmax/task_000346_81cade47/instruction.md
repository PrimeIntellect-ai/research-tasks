You are a penetration tester analyzing an intercepted package from a suspected vulnerable web server. You have been provided with a set of intercepted files in the `/home/user/pentest/` directory.

The directory contains three files:
1. `auth_capture.txt`: An intercepted HTTP request header file containing an authentication token.
2. `server.bin`: An encrypted binary payload found on the server.
3. `server.crt`: The server's public TLS certificate.

Your task is to write a Python script at `/home/user/pentest/analyze.py` that performs the following steps:

1. **Authentication Flow & Payload Decoding**:
   - Read `auth_capture.txt` and extract the Bearer token (the string following `Authorization: Bearer `).
   - The token is a Base64-encoded JSON object. Decode it.
   - Extract the `client_id` and the `file_hash` fields from the decoded JSON.

2. **File Integrity Verification**:
   - Calculate the SHA-256 hash of the `server.bin` file.
   - Compare your calculated hash against the `file_hash` extracted from the token. Determine if the integrity is `Valid` (hashes match) or `Invalid` (hashes do not match).

3. **TLS/SSL Certificate Management**:
   - Parse the `server.crt` file to extract the Common Name (CN) of the **Issuer** of the certificate. (You may use Python's built-in libraries or execute standard CLI tools like `openssl` from within your script).

4. **Reporting**:
   - Write the results to a log file located at `/home/user/pentest/report.txt`.
   - The log file must be in the exact following format:
     ```
     Client ID: <extracted_client_id>
     Integrity: <Valid or Invalid>
     Certificate Issuer CN: <extracted_issuer_cn>
     ```

Run your Python script to generate the `/home/user/pentest/report.txt` file so that your results can be verified.