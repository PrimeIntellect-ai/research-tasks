You are a DevSecOps engineer tasked with implementing a "policy-as-code" automated test suite. A new file upload microservice has been proposed, and you need to write a Bash-based security testing script to evaluate it for authentication enforcement, encrypted credential handling, and path traversal vulnerabilities before it reaches production.

You have been provided with the service code at `/home/user/upload_server.py` and its dependencies. The service runs on port 8080. 

Your objective is to write a Bash test script at `/home/user/run_policy.sh` that performs the following automated checks against the running server, and then writes a JSON report of the findings.

Here are the requirements for your testing procedure:

1. **Environment Initialization:**
   - Install `flask` and `werkzeug` (e.g., `pip install flask werkzeug`).
   - Start the server `/home/user/upload_server.py` in the background on port 8080.

2. **Credential Decryption:**
   - The service requires a Bearer token for authentication.
   - The token is encrypted using AES-256-CBC and stored at `/home/user/credentials/token.enc`.
   - The passphrase to decrypt it is located at `/home/user/credentials/pass.txt`.
   - Your script must decrypt this token dynamically (using `openssl enc -aes-256-cbc -d -pbkdf2 -in ... -pass file:...`) to use in subsequent requests.

3. **Authentication Flow Testing:**
   - Attempt to POST a benign file (e.g., `test.txt`) to `http://127.0.0.1:8080/upload` *without* an `Authorization: Bearer <token>` header. Record the HTTP status code.
   - Attempt the same POST *with* the decrypted Bearer token. Record the HTTP status code.

4. **Path Traversal & Integrity Verification:**
   - There is a highly sensitive file located at `/home/user/system/critical_config.txt`.
   - Calculate and record the SHA-256 hash of this file *before* the attack.
   - Using the authenticated Bearer token, attempt to exploit a path traversal vulnerability in the upload endpoint. The API accepts a `filename` form field. Craft a payload that attempts to overwrite `/home/user/system/critical_config.txt` with the text "PWNED".
   - After the upload attempt, calculate the SHA-256 hash of `/home/user/system/critical_config.txt` again. 
   - Determine if the file integrity was compromised (i.e., if the hash changed).

5. **Reporting:**
   - Your script must generate a report at `/home/user/policy_report.json` with exactly the following keys and correct extracted/computed values:
     ```json
     {
       "auth_missing_status": <integer HTTP status code when token is missing>,
       "auth_provided_status": <integer HTTP status code with valid token>,
       "pre_attack_hash": "<SHA-256 hash of critical_config.txt before attack>",
       "post_attack_hash": "<SHA-256 hash of critical_config.txt after attack>",
       "is_vulnerable": <true or false (boolean, true if hashes differ)>
     }
     ```

Make sure `/home/user/run_policy.sh` is executable and runs seamlessly. Run your script to generate the final `/home/user/policy_report.json`.