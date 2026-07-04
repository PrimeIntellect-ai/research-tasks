You are a network security engineer investigating a potentially compromised embedded device on your network. You have extracted a capture of its configuration and keys to your local machine.

You suspect the device's administrator made a critical security error by reusing their SSH private key for the web server's TLS certificate. Additionally, you have found an undocumented API endpoint that grants remote command execution if a request is signed with this reused key.

Your task is to analyze the extracted files, verify the certificate chain, identify the reused key, and craft the exploit payload.

The extracted files are located in: `/home/user/investigation/`
- `ca.crt`: The root Certificate Authority.
- `intermediate.crt`: The intermediate CA.
- `server.crt`: The device's web server TLS certificate.
- `ssh_keys/`: A directory containing three captured SSH private keys (`id_rsa_A`, `id_rsa_B`, `id_rsa_C`).

Perform the following steps using standard Bash and CLI tools (like `openssl` and `ssh-keygen`):

1. **Certificate Chain Validation:**
   Verify if `server.crt` is validly signed by the `ca.crt` through the `intermediate.crt`. 
   Save the exact output of the standard `openssl verify` command (e.g., "server.crt: OK" or the specific error) to `/home/user/cert_status.txt`.

2. **Key Identification:**
   Determine which of the three SSH private keys in `/home/user/investigation/ssh_keys/` matches the public key embedded in `server.crt`.
   Write the base filename of the matching key (e.g., `id_rsa_A`) to `/home/user/matched_key.txt`.

3. **Exploit Crafting:**
   The undocumented API requires a signed payload to grant access. The plaintext payload string is exactly:
   `user=admin&action=shell`
   
   Using the matched SSH private key, sign this exact string using RSA with the SHA256 digest algorithm. 
   Encode the resulting binary signature in Base64.
   Save the final exploit header to `/home/user/payload.txt` in the following exact format:
   `X-Auth-Signature: <your_base64_string>`

Note: Do not append any newlines to the plaintext payload string before signing.