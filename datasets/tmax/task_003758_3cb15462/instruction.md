You are a security engineer tasked with rotating credentials for an old file upload microservice. The service previously suffered from a path traversal vulnerability because compromised tokens allowed attackers to bypass input validation.

To rotate the credentials, you need to generate a new authentication token. Unfortunately, the token generation script has been lost, and the only artifact remaining is the compiled token validator binary: `/home/user/upload_auth.bin`.

Your task is as follows:
1. Analyze the ELF binary `/home/user/upload_auth.bin` to find a hardcoded 16-character salt. It is stored in the read-only data section immediately following the exact string `SALT:`.
2. Write a C++ program at `/home/user/keygen.cpp` that generates the new token. The program must:
   - Include `<openssl/sha.h>` for hashing.
   - Concatenate the new password `"StrictPassword2024!"` and the 16-character salt extracted from the binary (format: `password` followed by `salt`).
   - Compute the SHA-256 hash of this concatenated string.
   - Output the resulting token to the file `/home/user/new_token.txt` exactly in the format: `AUTH-TOKEN-<lowercase_hex_encoded_sha256_hash>`.
3. Compile your C++ program to `/home/user/keygen` (make sure to link against the OpenSSL crypto library using `-lcrypto`) and execute it so that `/home/user/new_token.txt` is created with the correct token.

Ensure the final token file contains no trailing newlines or extra spaces.