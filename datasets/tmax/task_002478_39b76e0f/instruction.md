You are a forensics analyst investigating a compromised host. An attacker exploited a vulnerability in a custom, locally-hosted Python file storage service known as "FileVault" to escalate privileges and exfiltrate data. Your job is to recover the environment, identify and patch the vulnerability, uncover the attacker's credentials, and bring the secured service back online for the incident response team to verify.

The vendored source code for the service is located at `/app/file_vault`. 

Here are your objectives:

1. **Fix the Vendored Package:**
   The attacker attempted to sabotage the service to prevent forensics. The installation files in `/app/file_vault` have been intentionally broken (there is a deliberate typo/error in the package dependencies). Fix the package configuration so it can be installed locally via `pip install -e /app/file_vault`.

2. **Recover the Admin Credentials (Password Cracking/Cryptanalysis):**
   The attacker dumped an encrypted admin access token in `/home/user/evidence/token.hex`. The encryption used is a custom, weak XOR cipher. The attacker's encryption script is partially recovered at `/home/user/evidence/encryptor.py`. Reverse-engineer the encryption, recover the plaintext admin token, and save it to `/home/user/evidence/recovered_token.txt`.

3. **Patch the Path Traversal and Token Validation:**
   Review the source code in `/app/file_vault/file_vault/server.py`. 
   - The `/upload` endpoint is susceptible to a path traversal attack. Patch the code so that any file name containing `../` or `/` is rejected with an HTTP 400 status code.
   - The token validation logic is broken. Update it so that the `/upload` endpoint requires an `Authorization: Bearer <token>` header, and only accepts the exact plaintext admin token you recovered in step 2. If the token is missing or incorrect, return an HTTP 401 status code.

4. **Deploy the Secured Service:**
   Start the patched FileVault HTTP server. It must listen on `127.0.0.1:9090`. 
   The service must save legitimate uploaded files to `/app/uploads/` (create this directory if it doesn't exist). 
   Leave the service running in the background. The automated verification suite will issue network requests to this port to ensure the traversal is blocked and authentication works properly.