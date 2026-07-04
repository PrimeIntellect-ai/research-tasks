You are a security engineer tasked with rotating credentials for a legacy web server. The junior developer who generated the new TLS private key left the company, leaving behind only a base64-encoded, encrypted private key and a list of possible passwords they commonly used. 

You need to recover the key, verify it matches the new certificate, and prepare a safely redacted version of the key for the documentation team.

Here is the environment you are working with:
- `/home/user/certs/ca.crt`: The internal Certificate Authority certificate.
- `/home/user/certs/server.crt`: The newly issued server certificate.
- `/home/user/certs/encrypted_key.b64`: A base64-encoded text file containing the encrypted RSA private key.
- `/home/user/wordlist.txt`: A text file containing a list of possible passwords (one per line).

Perform the following steps using Bash and standard Linux tools (like `openssl`, `base64`, `awk`/`sed`):
1. **Decode and Crack**: Base64-decode the `encrypted_key.b64` file. Then, brute-force the password using `wordlist.txt` to decrypt the private key. 
2. **Validate**: Ensure that the decrypted private key matches `server.crt`. Validate that `server.crt` is properly signed by `ca.crt`. (You do not need to output the validation result, but you must ensure they match).
3. **Extract Modulus**: Extract the MD5 hash of the public modulus of the decrypted private key. Write *only* this MD5 hash string (e.g., `a1b2c3d4...`) to `/home/user/modulus.txt`.
4. **Redact**: Create a redacted version of the *decrypted* private key at `/home/user/redacted.key`. The file must keep the `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----` lines exactly as they are, but all lines between them must be replaced by exactly one line containing only the word: `REDACTED`.

Make sure the files `/home/user/modulus.txt` and `/home/user/redacted.key` are formatted exactly as requested.