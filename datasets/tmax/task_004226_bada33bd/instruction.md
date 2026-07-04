You are an AI assistant helping a compliance analyst securely generate and store web server audit trails. Raw access logs often contain sensitive data in the query parameters of URLs, which must be redacted. Furthermore, the processing of these logs must be isolated to minimize the risk of untrusted data exploiting the log parser, and the final output must be encrypted at rest.

Your objective is to create a secure pipeline that redacts, encrypts, and safely stores these logs.

**Requirements:**

1. **Redaction Logic:** 
   Write a Bash script named `/home/user/process_logs.sh`. This script must read `/home/user/raw_logs/access.log` and redact the values of any query parameters named `api_key` or `card`. 
   For example, a request to `GET /api/v1/user?api_key=xyz123&card=41112222&action=view HTTP/1.1` should be transformed to `GET /api/v1/user?api_key=REDACTED&card=REDACTED&action=view HTTP/1.1`. Other query parameters must remain untouched.

2. **Encryption:**
   After redacting the log in memory or a temporary file, the script `/home/user/process_logs.sh` must encrypt the redacted content using OpenSSL. 
   - Cipher: AES-256-CBC
   - Key derivation function: PBKDF2
   - Salt: enabled
   - Passphrase file: Read from `/home/user/certs/audit_key.pem`
   The final encrypted file must be saved to `/home/user/audit_trail/secure_audit.log.enc`.

3. **Process Isolation (Sandboxing):**
   To execute the processing script securely, write a second script named `/home/user/run_sandbox.sh`. This script must use `bwrap` (Bubblewrap) to create an isolated environment with the following exact constraints:
   - Network namespace must be unshared (no network access).
   - The entire root filesystem `/` must be mounted read-only.
   - `/dev` must be mounted as a functional device tree (e.g., using `--dev`).
   - The directories `/home/user/raw_logs` and `/home/user/certs` must be mounted read-only.
   - The directory `/home/user/audit_trail` must be the ONLY user directory mounted with read-write access.
   - The sandbox must execute `/home/user/process_logs.sh` inside this restricted environment.

**Execution:**
Once you have written both scripts, execute `/home/user/run_sandbox.sh` to process the logs. Ensure both scripts are executable.

**Deliverables:**
- `/home/user/process_logs.sh` (containing redaction and encryption logic)
- `/home/user/run_sandbox.sh` (containing the sandbox execution wrapper)
- The successful generation of `/home/user/audit_trail/secure_audit.log.enc`