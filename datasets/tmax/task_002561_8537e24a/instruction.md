You are an incident responder investigating a suspicious custom token validation service on a compromised Linux machine. The attackers seem to have bypassed the authentication mechanism.

The service uses a custom C program to validate tokens. You need to investigate the environment, find the vulnerability, and prove it by crafting an exploit payload.

Here is your investigation checklist:

1. **File Integrity Verification:** 
   The original source code for the validator is located at `/home/user/validator.c`. Check its SHA-256 hash against the known good hash stored in `/home/user/checksum.sha256`. If it matches, compile it to `/home/user/validator` using `gcc /home/user/validator.c -o /home/user/validator`.

2. **Certificate Chain Validation:**
   The service uses a local certificate for identity verification. Verify that the server certificate `/home/user/server.crt` is validly signed by the certificate authority `/home/user/ca.crt`. Save the stdout output of the `openssl verify` command to `/home/user/cert_verify.log`.

3. **Vulnerability Analysis & Encryption:**
   Analyze `/home/user/validator.c`. The program expects a token passed as a command-line argument in the format:
   `<HexEncodedHeader>.<HexEncodedEncryptedPayload>.<HexEncodedSignature>`
   
   The program parses the JSON-like header and payload. The payload is encrypted using a simple XOR cipher (the key is hardcoded in the C source).
   Find the logical flaw that allows signature verification to be bypassed (similar to the JWT `alg=none` vulnerability).

4. **Exploit Crafting:**
   Craft a malicious token that:
   - Bypasses the signature verification check.
   - Contains an encrypted payload that decrypts to exactly `{"role":"admin"}`.
   - Has a dummy signature (e.g., `0000`).

5. **Reporting:**
   Save your successfully forged token (the exact string that you would pass to the validator) into the file `/home/user/forged_token.txt`.

Ensure all files are created exactly at the specified paths.