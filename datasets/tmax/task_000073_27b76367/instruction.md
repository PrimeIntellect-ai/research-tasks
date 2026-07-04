As a penetration tester, you have intercepted a video recording of an administrator's dashboard (`/app/dashboard_recording.mp4`). This video contains a brief frame (flashing for just a fraction of a second) that leaks two critical pieces of information in plain text:
1. `HMAC_SECRET`: A string used for symmetric JWT signing.
2. `TRUSTED_FINGERPRINT`: The SHA-256 fingerprint of the organization's trusted root certificate.

Your objective is to build a robust JWT validator that patches several vulnerabilities found in the system, including "alg: none" bypasses and privilege escalation. 

First, use tools like `ffmpeg` and `tesseract-ocr` (which you can install) to extract the `HMAC_SECRET` and `TRUSTED_FINGERPRINT` from the video.

Next, create a Python script at `/home/user/jwt_filter.py` that takes a single command-line argument: the path to a file containing a raw JWT string.
Your script must exit with status code `0` if the JWT is "clean" (valid and secure) and status code `1` if the JWT is "evil" (invalid, malicious, or insecure).

To be considered "clean", a JWT must meet ALL the following conditions:
1. **Algorithm Validation:** The `alg` header must NOT be `none` (case-insensitive). It must be either `HS256` or `RS256`.
2. **Signature Validation:** 
   - If `alg` is `HS256`, the signature must be valid using the `HMAC_SECRET` extracted from the video.
   - If `alg` is `RS256`, the token header will contain an `x5c` array with a single PEM-encoded X.509 certificate. The signature must be valid for this certificate, AND the SHA-256 fingerprint of this certificate must exactly match the `TRUSTED_FINGERPRINT` extracted from the video.
3. **Content Security Policy:** The token payload MUST contain a `csp` claim. The value of this claim must be exactly the string `default-src 'self'`.
4. **Privilege Escalation Audit:** If the token payload contains `"role": "admin"`, the token MUST use the `RS256` algorithm and be validated by the trusted certificate. (Admin tokens signed with the symmetric `HMAC_SECRET` are considered forged and must be rejected).

Your script will be tested against a hidden corpus of clean and evil JWTs. You must achieve 100% accuracy to pass. Ensure your script handles missing fields or malformed tokens gracefully by exiting with code 1.