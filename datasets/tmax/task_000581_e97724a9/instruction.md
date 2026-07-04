You are acting as a compliance analyst for a financial tech company. Your task is to generate a secure, sanitized audit trail from raw service logs and validate the authentication flows recorded within them.

This is a multi-stage workflow consisting of environment repair, token validation, and the development of an adversarial-resistant data redactor.

**Stage 1: Fix the Vendored Cryptography Package**
Our internal auditing scripts rely on a vendored version of the PyJWT library. However, a recent misconfiguration broke the package. 
The package is located at `/app/vendored/pyjwt-2.8.0/`. 
Find the deliberate perturbation that was introduced (it explicitly raises an error during standard decoding) and fix the source code so that JWT signature verification works correctly again. You will need to install this package locally (e.g., `pip install -e /app/vendored/pyjwt-2.8.0/`) after fixing it to use it in the next stages.

**Stage 2: Authentication Flow Validation**
There is a file containing raw authentication tokens at `/home/user/captured_tokens.txt`. The HMAC-SHA256 symmetric secret used by our system is stored in `/home/user/jwt_secret.key`.
Write a script to validate these tokens using the fixed PyJWT package. Identify all tokens with valid signatures and unexpired claims. Write the `user_id` claim of every valid token to `/home/user/valid_users.log`, one per line, sorted alphabetically.

**Stage 3: Develop a Sensitive Data Redactor**
We must sanitize raw logs before storing them in our compliance archive. You need to write a Python script at `/home/user/redactor.py`.
Your redactor must accept two positional CLI arguments: an input file path and an output file path.
Invocation format: `python3 /home/user/redactor.py <input_file> <output_file>`

The redactor must read the input file line-by-line and replace any instance of the following sensitive data types with the exact string `[REDACTED]`:
1.  Credit Card Numbers (13-19 digits, potentially separated by dashes or spaces).
2.  AWS Access Key IDs (Starting with `AKIA` followed by 16 alphanumeric characters).
3.  Any raw JSON Web Tokens (JWTs) embedded in the log text (identified by the standard `ey...` Base64Url format).

*Crucially*, the redactor must NOT alter benign strings that look similar, such as git commit hashes, standard UUIDs, internal transaction IDs, or random debug hex strings. 
Your script will be tested against a hidden adversarial evaluation suite containing an "evil" corpus (logs full of sensitive data that must be redacted) and a "clean" corpus (benign logs that must remain completely unchanged).

**Stage 4: Generate the Final Audit Checksum**
Generate a SHA-256 checksum of your `/home/user/valid_users.log` file and save the hash (just the hex string) to `/home/user/audit_checksum.txt`.