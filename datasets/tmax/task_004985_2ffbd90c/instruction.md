You are a security engineer tasked with rotating credentials and building a robust JWT sanitizer for our legacy authentication system. The current system relies on an old authentication service where the public key was hardcoded, and the previous tokens have been compromised via "alg=none" and payload injection attacks. 

You need to complete the following multi-stage workflow:

1. **Extract Compromised Keys (Binary Analysis):**
   The legacy service binary is located at `/app/bin/legacy_auth_service`. An old 2048-bit RSA public key (in PEM format) is embedded directly in its `.rodata` section. Extract this public key and save it exactly as `/home/user/old_pub.pem`.

2. **Fix the Vendored Library:**
   Our system uses a vendored version of `PyJWT-1.7.1`, located at `/app/vendor/PyJWT-1.7.1`. A previous developer accidentally broke the RSA signature verification logic in this package during a botched patching attempt. Locate the deliberate perturbation in the RSA verification path, fix it so it properly verifies valid RS256 signatures, and install the package into your environment.

3. **Key Rotation (TLS & Cryptography):**
   Generate a new 2048-bit RSA key pair. Save the private key to `/home/user/new_key.pem`. Generate a self-signed x509 TLS certificate using this new key (valid for 365 days, Subject CN=`auth.local`). Save the certificate to `/home/user/new_cert.pem` and extract its public key to `/home/user/new_pub.pem`.

4. **Build the Intrusion Detection Filter:**
   Write a Python script at `/home/user/jwt_filter.py` that takes a single file path as a command-line argument. The file will contain a single raw JWT.
   The script must evaluate the token and print exactly `ACCEPT` or `REJECT` to stdout (and nothing else).
   
   A token MUST be `REJECT`ed if ANY of the following are true:
   - The token uses `alg=none` (or any case variation like `None`, `NONE`).
   - The token's signature successfully verifies against the COMPROMISED key (`/home/user/old_pub.pem`).
   - The decoded payload contains a `sub` or `role` claim that includes directory traversal patterns (e.g., `../`, `..\`) or common payload encoding bypasses like `%2e%2e%2f`.
   - The token is improperly formatted or cannot be decoded/verified securely.
   
   A token MUST be `ACCEPT`ed if:
   - It is a structurally valid JWT.
   - It uses a secure algorithm (e.g., `RS256`).
   - It is securely signed by the NEW key (`/home/user/new_key.pem`).
   - It does not contain malicious traversal patterns in its claims.

You must rely solely on standard Python libraries, your system tools, and the provided vendored package. We will test your script against a hidden dataset of tokens.