You have been hired as a security auditor to review and fix a vulnerable multi-service architecture located in `/home/user/app`. The system consists of an Nginx reverse proxy serving HTTPS and a backend authentication service written in C listening on TCP. 

Currently, the Nginx service proxy is misconfigured, the backend service uses weak encryption (which fails a linear cryptanalysis check built into our verification), and SSH keys for automated deployments have incorrect permissions.

Your tasks are:
1. **Fix the C Backend Service**: The source code is at `/home/user/app/backend.c`. It encrypts incoming user tokens over TCP. Currently, it uses a trivial XOR cipher that is vulnerable to cryptanalysis. Modify the encryption function to use a strong block cipher (e.g., AES-128-CBC via OpenSSL). Recompile it and ensure it listens on `127.0.0.1:8081`. The backend must accept connections, decrypt incoming tokens, and return a fixed session cookie header format: `Set-Cookie: session=<token>; Secure; HttpOnly`.
2. **Configure Nginx**: The Nginx configuration at `/home/user/app/nginx.conf` must be updated. It should listen on port `8443` using TLS. Use the existing self-signed certificate and key located in `/home/user/app/certs/`. Ensure it terminates TLS and correctly forwards traffic to the C backend on port `8081`. It must also inspect incoming HTTP headers and drop any requests lacking the `X-Auditor-Auth` header.
3. **Fix SSH Permissions**: The automated deployment SSH keys located at `/home/user/app/.ssh/id_rsa` and `/home/user/app/.ssh/id_rsa.pub` currently have overly permissive file permissions. Fix the permissions according to SSH hardening best practices.
4. **Service Startup**: Create a bash script at `/home/user/app/start.sh` that starts both the Nginx proxy (using the provided config) and the C backend service in the background.

When you are done, leave the services running by executing `/home/user/app/start.sh`.

Verification constraints:
- Nginx must listen on `127.0.0.1:8443` (HTTPS).
- The backend must listen on `127.0.0.1:8081` (TCP).
- The SSH private key must have `0600` permissions.
- Nginx must enforce the `X-Auditor-Auth` header.
- The C backend must use OpenSSL AES-128-CBC for token handling.