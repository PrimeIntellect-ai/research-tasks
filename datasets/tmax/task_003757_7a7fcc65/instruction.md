You are a forensics incident responder investigating a compromised host. We have recovered a custom malware implant, a stripped ELF binary located at `/app/implant_c2`. 

Network logs indicate this binary acts as a Command and Control (C2) endpoint, receiving exfiltrated data via HTTPS POST requests. We need you to reverse engineer the binary's authentication and encryption mechanisms and build a honeypot server in Python to replace it, allowing us to safely capture and log incoming requests from other infected nodes.

Here are your instructions:

1. **Reverse Engineering:**
   Analyze `/app/implant_c2`. Identify the hardcoded Authentication Token and the Encryption Key. The malware uses the RC4 stream cipher to decrypt incoming payloads.

2. **TLS Certificate Management:**
   Generate a self-signed TLS certificate. Save the certificate to `/home/user/certs/server.crt` and the private key to `/home/user/certs/server.key`. Ensure the `certs` directory exists.

3. **Honeypot Implementation:**
   Create a Python script at `/home/user/c2_honeypot.py` that implements an HTTPS server listening on `127.0.0.1:8443` using the TLS certificates you generated. It must handle `POST` requests to the `/exfil` endpoint.

4. **Authentication Flow:**
   The server must check for the `X-Auth-Token` HTTP header. If the header is missing or does not exactly match the authentication token you extracted from the binary, the server must immediately respond with an HTTP `401 Unauthorized` status and an empty body.

5. **Decryption and Sensitive Data Redaction:**
   If authenticated, the server must read the raw binary POST body and decrypt it using RC4 and the encryption key you extracted. 
   The decrypted payload is a UTF-8 string. This string may contain sensitive credit card numbers (exactly 16 consecutive digits, e.g., `1234567812345678`). You must redact these by replacing the 16 digits entirely with the string `[REDACTED_CC]`. 

6. **Logging and Response:**
   Append the fully decrypted and redacted UTF-8 string to `/home/user/exfil_log.txt`, followed by a newline (`\n`). 
   Finally, the server must respond with an HTTP `200 OK` status and the exact text body: `ACK: <length_of_redacted_text_in_bytes>`.

Execute your Python server in the background so it remains running. Our automated verification system will send requests to `https://127.0.0.1:8443/exfil` to test your honeypot's authentication, decryption, and redaction logic.