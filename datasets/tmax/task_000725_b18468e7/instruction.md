You are a security auditor tasked with checking the permission logic of a legacy internal authentication service. As part of your audit, you must repair a broken vendored library, then implement a bit-exact replacement for the permission evaluation script so it can be aggressively fuzzed against a known-good reference oracle.

Step 1: Fix the Vendored Package
The system uses a custom C-extension for Python to handle proprietary Base64 decoding, located at `/app/custom_b64-1.0`. The developers introduced a deliberate perturbation: the `setup.py` file has an incorrect source file listed (it points to `wrong_source.c` instead of `custom_b64.c`). 
Fix the `setup.py`, compile, and install the package into your Python environment.

Step 2: Implement the Permission Checker
Write a multi-language wrapper (preferably a Python script at `/home/user/check_permissions.py`) that acts exactly like our reference binary.
Your script must:
1. Read a raw HTTP request from `stdin` until EOF.
2. Inspect the HTTP headers to find the `X-Secure-Auth` header.
3. Decode the value of `X-Secure-Auth` using the installed `custom_b64.decode(payload)` function. The decoded payload will be a pipe-separated string: `username|role|cert_sha256_hex`.
4. Read the TLS certificate from `/app/server.crt`, parse it, and compute its SHA-256 fingerprint (hexadecimal, lowercase).
5. Compare the parsed `cert_sha256_hex` from the token against the actual certificate's fingerprint.
6. Evaluate the permission:
   - If the HTTP headers do not contain `X-Secure-Auth`, print exactly `DENY:MISSING_HEADER`.
   - If `custom_b64.decode()` raises an exception (e.g. invalid encoding), print exactly `ERROR:DECODE_FAIL`.
   - If the certificate fingerprint does not match the parsed payload, print exactly `DENY:CERT_MISMATCH`.
   - If the fingerprint matches and the role is exactly `admin`, print exactly `GRANT:ADMIN`.
   - If the fingerprint matches and the role is anything else, print exactly `GRANT:USER`.
7. Your script must process the input and terminate correctly.

Your program will be verified using differential fuzzing against our internal oracle `/app/oracle_checker`. Ensure your output format matches the specifications precisely.