You are a security engineer tasked with rotating a compromised API credential. An incident occurred where an encrypted admin token was leaked in the web server's access logs, and an attacker successfully used it.

Your task is to identify the leaked token, decrypt it, generate a new token, encrypt the new token, and hash the new token. You must write a C++ program to perform the cryptographic operations.

**Task details:**
1. Analyze the log file at `/home/user/access.log`. The file contains multiple HTTP requests. Find the base64-encoded encrypted token passed in the `token` query parameter to the `/api/admin` endpoint that resulted in a successful `200 OK` HTTP status. Discard any requests that resulted in other status codes (e.g., 400, 403, 404).
2. The encryption key and initialization vector (IV) used for the token are 16 bytes each. They are stored in plain text in `/home/user/key.txt` and `/home/user/iv.txt`, respectively.
3. Write a C++ program (e.g., `rotate.cpp`) that uses the OpenSSL library (`libcrypto`) to:
   - Base64 decode and decrypt the leaked token. The encryption algorithm is AES-128-CBC with standard PKCS7 padding.
   - Generate a new token by appending the exact string `_rotated` to the decrypted leaked token.
   - Encrypt the new token using AES-128-CBC with the same key, IV, and PKCS7 padding.
   - Base64 encode the new encrypted token.
   - Compute the SHA-256 hash of the *new decrypted token* (the plaintext version ending in `_rotated`), formatted as a lowercase hexadecimal string.
4. Compile and run your C++ program. You may install necessary dependencies like `libssl-dev` using `sudo apt-get` if they are not present.
5. Your C++ program (or a wrapper script) must output the final results to `/home/user/rotation_result.txt` in exactly the following format:

```text
Leaked: <decrypted_old_token_plaintext>
New_Encrypted: <base64_encoded_new_encrypted_token>
New_Hash: <sha256_hex_of_new_decrypted_token>
```

Ensure the file `/home/user/rotation_result.txt` exists and strictly follows the format above. Only the token that received a `200` status code should be processed.