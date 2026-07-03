You are a compliance analyst responsible for generating audit trails and preventing credential leakage in our infrastructure. We have discovered that some services are accidentally passing sensitive access tokens (JWTs) via command-line arguments, which exposes them in `/proc/<pid>/cmdline` to any user on the system. 

Your objective is to write a Python script that analyzes process command lines and detects legitimate token leaks.

1. **Write a detector script** at `/home/user/audit_filter.py`. 
   - The script must take a single command-line argument: the path to a file containing a process's command line (formatted exactly like `/proc/<pid>/cmdline`, with null-byte `\0` separated arguments).
   - The script must extract any string that structurally resembles a JWT (three base64-url encoded segments separated by dots).
   - To distinguish real tokens from random strings or forged tokens, the script must mathematically validate the JWT's RS256 signature.
   - **Certificate Chain Validation**: The system uses a PKI. You are provided with `/app/certs/ca.crt` (the root CA) and `/app/certs/leaf.crt` (the issuing cert). Before trusting `leaf.crt`'s public key, your script MUST verify that `leaf.crt` was validly signed by `ca.crt`. (You may use `openssl` via `subprocess`, or any standard Python library to do this validation check in your script).
   - Once the certificate chain is verified, extract the public key from `leaf.crt` and use it to verify the JWT signature.
   - If a syntactically correct JWT is found AND it has a valid signature matching the trusted leaf certificate, your script must print exactly `LEAK` to standard output and exit with status 0.
   - If no JWT is found, or the JWT signature is invalid, or the certificate chain is invalid, your script must print exactly `CLEAN` to standard output and exit with status 0.

2. **Fix the Vendored JWT Library**:
   - For security isolation, you must use the locally vendored version of the PyJWT library located at `/app/PyJWT-2.6.0`. Do not install external packages from PyPI.
   - Ensure your script uses this exact package (e.g., by manipulating `sys.path`).
   - *Note:* The vendored PyJWT package has a known corruption in its codebase introduced by a faulty internal sync. You will need to inspect and patch the RSA validation logic in `/app/PyJWT-2.6.0/jwt/algorithms.py` so that it correctly verifies RS256 signatures again.

Your script will be tested against two sets of command-line dumps: an "evil" corpus containing actual leaks, and a "clean" corpus containing normal traffic and failed forgery attempts. Your detector must correctly identify 100% of both corpora.