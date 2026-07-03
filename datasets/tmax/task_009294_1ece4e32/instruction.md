You are a compliance analyst responsible for generating verifiable security audit trails. We suspect our internal authentication service has an open redirect vulnerability in its login flow that could be used for phishing and cookie theft. 

Your task is to write a C++ program that programmatically verifies this vulnerability, inspects the HTTP headers, and generates a cryptographically hashed audit log.

1. Start the simulated vulnerable authentication service in the background. The service script is located at `/home/user/auth_service.py`. It runs on `127.0.0.1:8000`.
2. Write a C++ program at `/home/user/generate_audit.cpp`. This program must:
   - Create a raw TCP socket and connect to `127.0.0.1:8000`.
   - Craft and deliver an HTTP GET request to the vulnerable endpoint: `/login?next=http://attacker.com/steal_cookie`. Ensure you include valid HTTP/1.1 syntax and a `Host` header.
   - Read the HTTP response and parse the headers to find the exact value of the `Location` header.
   - Compute the SHA-256 hash of the extracted URL string (e.g., using OpenSSL's `<openssl/sha.h>`, compile with `-lcrypto`).
   - Create an audit log file at `/home/user/audit_trail.txt` containing exactly one line in the following format:
     `OPEN_REDIRECT_VERIFIED: <extracted_url> | SHA256: <hex_encoded_sha256_hash>`

Ensure your C++ code correctly handles socket creation, HTTP parsing, and hex-encoding the cryptographic hash. Once your code is written, compile it to `/home/user/generate_audit`, run it, and ensure `/home/user/audit_trail.txt` is generated exactly as specified.