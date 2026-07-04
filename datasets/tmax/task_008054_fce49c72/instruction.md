You are a security engineer tasked with rotating credentials for a legacy service after a suspected data leak. The legacy service uses a custom JSON Web Token (cJWT) implementation. 

You have been provided with the following files in `/home/user/`:
1. `auth_logic.py`: An obfuscated Python script containing the legacy token verification logic.
2. `server_logs.txt`: A log file containing access records, some of which leaked valid custom JWTs.
3. `wordlist.txt`: A small dictionary of words used by the legacy system to select its signing secret.

Your objectives are:

**Phase 1: Reverse Engineering & Password Cracking**
Deobfuscate `auth_logic.py` to understand how the token signature is generated. Analyze the leaked tokens in `server_logs.txt`. Knowing that the secret used to sign the tokens is exactly one of the words in `wordlist.txt`, brute-force the secret by validating the signature of a leaked token.

**Phase 2: Payload Encoding**
Using the cracked secret, forge a new custom JWT for the admin user to trigger a credential rotation. 
The new token must have exactly this header: `{"alg":"md5","typ":"cJWT"}`
The new token must have exactly this payload: `{"user":"admin","action":"rotate_credentials"}`
Both the header and payload must be encoded using URL-safe Base64 without padding (standard for JWTs). The signature must be calculated exactly as discovered in Phase 1.
Save this single, forged token string into `/home/user/new_admin_token.txt`.

**Phase 3: Sensitive Data Redaction**
Clean up the data leak. Read `/home/user/server_logs.txt` and replace every instance of a custom JWT (which follows the format `Header.Payload.Signature`) with the exact string `[REDACTED]`. Keep the rest of the log lines exactly the same.
Save the cleaned logs to `/home/user/server_logs_redacted.txt`.

Constraints:
- You may use any programming language you prefer to write your cracking, forging, or redaction scripts.
- Do not modify the original `server_logs.txt`.
- Ensure your forged token in `new_admin_token.txt` contains no trailing newlines or extra spaces.