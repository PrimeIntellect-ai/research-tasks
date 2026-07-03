You are a security auditor tasked with reviewing a compromised server's API traffic dump to find a specific authorization token that grants auditor access.

You have been provided with the following files:
1. `/home/user/.ssh/id_rsa.pub` - A public SSH key found on the server.
2. `/home/user/api_dump.enc` - An encrypted dump of HTTP requests.

Follow these steps to complete your audit:

**Step 1: Decrypt the API dump**
The file `api_dump.enc` was encrypted using OpenSSL's AES-256-CBC algorithm with PBKDF2 (`-pbkdf2`). 
The password used for encryption is the MD5 fingerprint of the SSH public key `/home/user/.ssh/id_rsa.pub`, with all colons (`:`) removed (for example, if the fingerprint is `MD5:11:22:33...`, the password is `112233...`).
Decrypt this file to a plaintext file named `/home/user/api_dump.txt`.

**Step 2: Inspect HTTP headers and Validate Tokens (C++)**
The decrypted file contains several raw HTTP requests. 
Write a C++ program named `/home/user/parser.cpp` (and compile it to `/home/user/parser`) that:
1. Reads `/home/user/api_dump.txt`.
2. Inspects the HTTP headers to extract all tokens provided in the `Authorization: Bearer <token>` headers.
3. The extracted tokens are hex-encoded ASCII strings. Your C++ program must hex-decode these tokens.
4. Validate the tokens by searching for the exact substring `PERM=GRANT_AUDIT` in the decoded ASCII text.
5. Once the valid token is found, write the **original hex-encoded token** string to `/home/user/audit_token.txt`.

Your final output must be just the hex-encoded token inside `/home/user/audit_token.txt`, with no additional whitespace or newlines.