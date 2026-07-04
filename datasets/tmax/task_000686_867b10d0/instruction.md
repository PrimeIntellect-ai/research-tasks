You are a security engineer tasked with securing a legacy credential rotation system. The system handles uploading and rotating sensitive TLS certificates and keys, but it is currently vulnerable to path traversal and uses insecure authentication.

The environment is located in `/app/` and contains the following components:
- An Nginx reverse proxy.
- A legacy backend service written in C (FastCGI).

Your objective involves several distinct phases: reverse engineering, TLS configuration, and building a robust C-based input sanitizer.

**Phase 1: Reverse Engineering & Password Recovery**
The system uses a standalone binary at `/app/bin/auth_module` to validate administrative rotation requests. The developer hardcoded an MD5 hash of the admin password into this binary.
1. Reverse engineer or inspect `/app/bin/auth_module` to extract the hardcoded MD5 hash.
2. Crack the hash (it is a common weak password found in standard wordlists like rockyou).
3. Save the cracked plaintext password in a new file exactly at `/app/config/admin_pass.txt`.

**Phase 2: Service Configuration & TLS**
The Nginx server currently listens on HTTP port 8080 without encryption.
1. Generate a self-signed TLS certificate for the domain `rotation.local`.
2. Save the certificate and private key to `/app/certs/cert.pem` and `/app/certs/key.pem` respectively.
3. Modify the Nginx configuration located at `/app/nginx/nginx.conf` so that it listens on port 8443 with TLS enabled, proxying requests to the backend on `127.0.0.1:9000`.
4. Start the services using the provided `/app/start.sh` script. Ensure both Nginx and the backend are running successfully.

**Phase 3: Path Traversal Sanitizer (Adversarial Corpus)**
The legacy backend's file upload handler is vulnerable to path traversal. Before we rewrite the backend, you must build a strict C-based filename sanitizer that we can deploy as a filter.
1. Write a C program at `/home/user/sanitizer.c` and compile it to `/home/user/sanitizer`.
2. The program must accept exactly one argument (the filename string) via `argv[1]`.
3. It must thoroughly analyze the filename for path traversal attempts, taking into account:
   - Standard dot-dot-slash (`../`, `..\`)
   - URL-encoded traversal (`%2e%2e%2f`, etc.)
   - Null byte injection
   - Absolute paths (starting with `/`)
4. If the filename is completely safe (contains only alphanumeric characters, dashes, underscores, and a single dot for the extension), the program should exit with status code `0`.
5. If the filename is suspicious or malicious, the program must exit with status code `1`.

*Note on Verification:* Your compiled `/home/user/sanitizer` binary will be tested against two hidden corpora: a `clean_corpus/` containing valid filenames, and an `evil_corpus/` containing highly obfuscated path traversal payloads. To succeed, your program must achieve a 100% rejection rate for the evil corpus and a 100% acceptance rate for the clean corpus.