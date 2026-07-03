You are a security engineer tasked with rotating the SSH credentials for a legacy service. 

The new SSH private key is securely packaged inside a custom JSON Web Token (JWT) located at `/home/user/legacy_token.jwt`. The company uses a custom C++ utility to validate tokens and extract credentials. The source code for this utility is provided at `/home/user/extractor.cpp`. 

However, the key rotation authority is temporarily offline, and you do not have the HMAC secret required to cryptographically sign or validate the token. 

Your objectives are:
1. Audit the source code in `/home/user/extractor.cpp` to identify a cryptographic logic vulnerability (CWE-327/CWE-287) related to token validation.
2. Exploit this vulnerability using standard Linux command-line tools to bypass the signature validation and extract the SSH private key from the JWT.
3. Install the extracted private key to `/home/user/.ssh/id_rsa`.
4. Apply standard SSH hardening permissions to the private key.
5. Generate the corresponding public key and save it to `/home/user/.ssh/id_rsa.pub`.

Complete the task using only the standard terminal shell and built-in tools. You may compile the C++ file if needed. 

Verify your success by ensuring that `/home/user/.ssh/id_rsa.pub` exists and is a valid SSH public key corresponding to the securely extracted private key.