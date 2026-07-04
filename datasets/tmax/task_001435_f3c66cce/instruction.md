You are a DevSecOps engineer tasked with enforcing "policy as code" for a legacy authentication microservice. The service relies on a vendored, heavily modified token validation package, but the latest deployment failed because the package source was corrupted, and a recent security audit flagged a critical vulnerability: the package accepts forged JSON Web Tokens (JWTs) using the "alg=none" bypass or null signatures.

Your objectives are as follows:

1. **Fix the Vendored Package:** 
   The source for the custom package `py-custom-jwt` (version 1.0.5) is located at `/app/py-custom-jwt-src`. The setup configuration has a deliberate perturbation that prevents it from being installed in our Python 3 environment. Identify the issue, fix the build configuration, and install the package locally.

2. **Service Auditing & Exploit Crafting:**
   Once the package is installed, analyze its `token_decode.py` module. The original logic fails to isolate the signature verification process properly. You must craft a malicious JWT payload that bypasses the signature check to elevate privileges. Generate a forged token claiming the role "superuser" (with `{"sub": "admin", "role": "superuser"}` in the payload) and write the exact base64-encoded token string to `/home/user/forged_token.txt`.

3. **Develop a Secure Policy Enforcer (Fuzz Equivalence):**
   To enforce strict policy checks going forward, you must write a standalone Python script located at `/home/user/secure_validator.py`. This script will act as a drop-in replacement for the validation logic. 
   
   Your script must take a single command-line argument (the JWT string) and perform strict cryptographic validation. It must ONLY accept tokens signed with the `HS256` algorithm using the secret key located at `/etc/app_secret.key`. Any invalid format, missing signature, "alg=none", or modified payload must result in an exit code of `1` and print exactly `INVALID` to stdout. A perfectly valid token must result in an exit code of `0` and print exactly `VALID` to stdout. 

   Your script's output and exit codes must be BIT-EXACT equivalent to our compiled reference oracle located at `/opt/oracle/secure_validator_oracle`. The automated testing suite will fuzz your script against the oracle with thousands of malformed, malicious, and valid tokens to ensure your policy enforcer is cryptographically secure and handles all edge cases identically.