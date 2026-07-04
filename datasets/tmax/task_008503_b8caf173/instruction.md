You are a DevSecOps engineer responsible for enforcing "Policy as Code" for a legacy application environment. Your objective is to write a comprehensive Bash automation script that audits the environment, remediates missing security controls, and creates a secure, isolated execution wrapper for the legacy service. 

Write and execute a Bash script named `/home/user/enforce_policy.sh` that performs the following steps automatically:

1. **TLS Certificate Management:**
   - Create a directory `/home/user/certs/`.
   - Generate a self-signed RSA-2048 TLS certificate (`server.crt`) and private key (`server.key`) in this directory. The certificate must be valid for exactly 365 days and have the Common Name (CN) set to `secure-legacy.local`.

2. **Token Generation:**
   - Read the secret string from `/home/user/secret.txt`.
   - Generate an HMAC-SHA256 signature for the exact string payload `user=admin` using the secret from the file.
   - Save the resulting hex-encoded HMAC string to `/home/user/auth_token.txt`. Format it as just the hex string (no extra spaces or filename output from openssl).

3. **Privilege Escalation & Vulnerability Auditing:**
   - Recursively scan the directory `/home/user/app/` for any files that pose a security risk. Specifically, find:
     a) Files with the SUID bit set.
     b) Files that are world-writable (writable by 'others').
   - Output the absolute paths of all such vulnerable files to `/home/user/audit_report.txt`, with one path per line. Sort the output alphabetically.

4. **Process Isolation (Sandboxing Wrapper):**
   - Create a wrapper script at `/home/user/run_secure.sh` and make it executable.
   - This wrapper script must execute the legacy service `/home/user/app/server.py` with strict isolation:
     a) It must enforce a maximum file descriptor limit of 50 (`ulimit -n 50`).
     b) It must run the python script in a completely cleared environment (using `env -i`), exposing ONLY two environment variables: 
        - `PATH=/usr/bin:/bin`
        - `AUTH_TOKEN` (whose value must be read from `/home/user/auth_token.txt` at runtime).

Ensure your script `/home/user/enforce_policy.sh` is executable and run it so that all artifacts (`certs/`, `auth_token.txt`, `audit_report.txt`, and `run_secure.sh`) are generated.