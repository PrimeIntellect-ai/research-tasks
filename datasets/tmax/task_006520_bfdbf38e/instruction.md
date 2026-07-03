You are a security engineer tasked with rotating credentials and sanitizing legacy data payloads for an internal microservice. 

You need to write a Go program located at `/home/user/rotator/main.go` that performs the following steps:

1. **Certificate Chain Validation:** 
   Verify the newly rotated certificate chain located in `/home/user/certs/`. 
   The directory contains `root.crt`, `sub.crt`, and `leaf.crt`. Your Go program must load these PEM-encoded certificates and verify that `leaf.crt` is validly signed by `sub.crt`, which in turn is signed by `root.crt`. 
   *If the chain is invalid, your program must exit with a non-zero status code and print an error.*

2. **Payload Decoding & Processing:**
   Read all JSON files in `/home/user/payloads/input/`. 
   Each file has the following format: `{"id": "<string>", "data_b64": "<base64_encoded_string>"}`.
   Decode the `data_b64` field. The decoded string is itself a JSON object containing `user`, `ssn`, and `old_token` fields.

3. **Sensitive Data Redaction:**
   In the decoded inner JSON payload, redact the `ssn` field. Replace all digits with `X` while preserving the dashes (e.g., `123-45-6789` becomes `XXX-XX-XXXX`).

4. **Token Generation:**
   Generate a new HS256 JWT (JSON Web Token) to replace the `old_token`.
   The new JWT must use the HMAC secret `SuperSecretRotationKey2024!`.
   The JWT header must be `{"alg":"HS256","typ":"JWT"}`.
   The JWT payload must be exactly: `{"user": "<user_from_payload>", "role": "admin", "exp": 1893456000}`.
   Replace the `old_token` field in the inner JSON with this new JWT. *You may use a standard Go JWT library or implement the HS256 signature manually.*

5. **Payload Encoding & Output:**
   Re-encode the modified inner JSON object back to a base64 string.
   Save the updated outer JSON payload to `/home/user/payloads/output/` using the exact same filename as the input. The output format must be `{"id": "<string>", "data_b64": "<new_base64>"}`.

6. **Summary Log:**
   Write a plain text file to `/home/user/rotation_summary.txt` containing exactly one line:
   `Successfully processed: <N> payloads` (where `<N>` is the number of files processed).

Compile your Go program and run it to process the data. Ensure all output files and the summary text file are created successfully.