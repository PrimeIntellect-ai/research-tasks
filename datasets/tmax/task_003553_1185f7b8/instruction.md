You are a security engineer tasked with rotating compromised credentials and implementing a strict token validation filter to protect a legacy microservice architecture.

Our system currently relies on a custom JSON Web Token-like format, but we recently discovered it is vulnerable to 'alg=none' attacks and weak key exploitation. You must complete a multi-phase remediation.

### Phase 1: Credential Rotation & File Security
The new credentials for rotation are inside an encrypted zip archive at `/app/keys/new_creds.zip`. 
1. The password for the zip file is weak and can be cracked using the dictionary provided at `/app/wordlist.txt`.
2. Crack the zip file and extract the new certificates (`root_ca.pem`, `leaf_cert.pem`, and `leaf_cert.key`) into `/app/keys/`.
3. Set strict file access controls: you must enforce `0400` permissions on `/app/keys/leaf_cert.pem` and `/app/keys/root_ca.pem`. Your validator application (built in Phase 2) must explicitly check the file permission of `/app/keys/leaf_cert.pem` using `stat()` and exit with a failure code if the permissions are not exactly `0400`.

### Phase 2: Token Validator implementation (C)
Write a standalone CLI tool in C at `/app/validator.c` and compile it to `/app/validator`. 
The validator must take exactly one argument: the path to a file containing a token.
Invocation: `/app/validator <path_to_token_file>`
The token format is a simplified JWT: `Base64(Header).Base64(Payload).Base64(Signature)`

Your validator MUST perform the following checks, and exit with code `0` (Success) if ALL checks pass, or exit with code `1` (Reject) if ANY check fails:
1. Parse the JSON Header. If the `alg` field is set to `"none"`, reject the token immediately.
2. Verify the certificate chain: The token's signature must be verified against `/app/keys/leaf_cert.pem`. Before using the leaf certificate, your code must programmatically verify that it is validly signed by `/app/keys/root_ca.pem` (Certificate Chain Validation). 
3. Verify the token signature (SHA256 with RSA) using the public key from the validated leaf certificate.
4. Ensure the leaf certificate has `0400` permissions on disk.

*(You may use OpenSSL `libcrypto` and `libssl` as well as standard JSON libraries like `cJSON` - you can install them via standard apt commands).*

### Phase 3: Service Composition & Reconfiguration
The environment has three services defined in `/app/start_services.sh` that must work together:
* **Nginx** (Frontend Proxy, port 8080)
* **Token Issuer** (Python Flask, port 8081)
* **Backend API** (Python Flask, port 8082)

1. Modify `/etc/nginx/nginx.conf` (or default site) to proxy requests for `/auth` to the Token Issuer, and `/api` to the Backend API.
2. Update `/app/backend/server.py` to point to your new `/app/validator` binary. (The backend service already contains logic to invoke a binary and check its exit code).
3. Ensure that the end-to-end flow succeeds. When configured correctly, the following flow must yield an HTTP 200 response with the text `"SECURE_DATA_ACCESSED"`:
`TOKEN=$(curl -s http://127.0.0.1:8080/auth); curl -s -H "Token: $TOKEN" http://127.0.0.1:8080/api/data`

There are two corpora of tokens provided at `/app/corpus/clean/` and `/app/corpus/evil/`. You must use these to test your validator. The `evil` corpus contains tokens with alg=none, tokens signed by the old compromised keys, and invalid cert chains.