You are acting as a DevSecOps engineer tasked with enforcing policy as code and securing a legacy microservice architecture.

The application stack resides in `/app/` and consists of three components:
1. An OpenSSH server running on a non-standard port (2222) for administrative access.
2. A custom API service written in C (`/app/src/api.c`) listening on port 8080.
3. An Nginx reverse proxy listening on port 8000.

Currently, the stack suffers from multiple security issues and misconfigurations. Your objective is to secure the services, fix the code vulnerabilities, and properly wire the services together. 

Here are your specific instructions:

1. **Code Auditing & Vulnerability Remediation (C)**: 
   The custom C API service in `/app/src/api.c` has a severe stack-based buffer overflow vulnerability (CWE-121) when parsing the `User-Agent` HTTP header. 
   - Identify the vulnerable function (e.g., `strcpy`, `sprintf`) and replace it with a secure alternative (e.g., `strncpy`, `snprintf`) to ensure headers of any length do not crash the service.
   - Recompile the executable by running `make` in `/app/src/`, which will output the binary to `/app/bin/api`.

2. **Service Composition**:
   The Nginx configuration file at `/app/nginx.conf` is incomplete. 
   - Modify it so that any HTTP requests to the path `/api/` (e.g., `http://127.0.0.1:8000/api/health`) are correctly reverse-proxied to the C API running at `http://127.0.0.1:8080/`.

3. **SSH Hardening**:
   The SSH daemon configuration at `/app/sshd_config` is insecure. Apply the following hardening policies:
   - Disable password authentication (`PasswordAuthentication no`).
   - Disable root login completely (`PermitRootLogin no`).
   - Restrict SSH access so only the user `devsecops` is allowed to log in (`AllowUsers devsecops`).
   - Enforce the use of Ed25519 host keys only (remove or comment out any `HostKey` directives for RSA or ECDSA, and ensure `HostKey /app/keys/ssh_host_ed25519_key` is the only active host key).

4. **File Integrity Verification**:
   To enforce build integrity, calculate the SHA-256 hash of your newly compiled executable (`/app/bin/api`). Write ONLY the SHA-256 hex digest to `/app/integrity.txt` (the file should contain exactly the 64-character hash string and an optional newline, nothing else).

5. **Deployment**:
   Once all the above steps are completed, start the services by running the provided script: `bash /app/start.sh`. Leave the services running so they can be verified.

Ensure your compiled C application remains robust against excessively long inputs and correctly replies to valid HTTP requests with its expected JSON payloads.