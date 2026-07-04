You are a security engineer tasked with rotating compromised credentials and patching a vulnerable login server. Our internal authentication server was recently targeted. We suspect an open redirect vulnerability in the login flow was used in combination with stolen credentials. 

Your objectives are:

1. **Security Log Parsing & Credential Revocation:**
   Analyze the web server logs at `/app/logs/server.log` to identify the leaked administrative token (look for multiple anomalous logins from the IP `192.168.1.100`). Write the compromised token to `/app/revoked_tokens.txt`.

2. **SSH Hardening & Key Management:**
   Generate a new ed25519 SSH keypair at `/home/user/.ssh/admin_key`. Ensure the private key has the correct file permissions (0600). Add the public key to `/home/user/.ssh/authorized_keys`. Remove any existing compromised keys from `authorized_keys`.

3. **Patching the Vendored Package:**
   The authentication server uses a vendored package located at `/app/vendored_auth/secure-auth-server-1.2.0/`. 
   It contains an open redirect vulnerability in `login.py`. Specifically, it blindly redirects users to the `next` query parameter after login.
   Modify `login.py` so that if the `next` parameter contains an absolute URL (e.g., starts with `http://` or `https://`), it defaults to redirecting to `/dashboard`. Relative paths (e.g., `/settings`) should still be allowed.
   The package also has a broken environment variable load in `config.py`. It attempts to read `AUTH_KEY` but defaults to a hardcoded insecure key `insecure_default_key`. Fix it to raise a `ValueError` if `AUTH_KEY` is not present in the environment.

4. **Service Configuration & Startup:**
   Write a bash script at `/app/start_services.sh` that:
   - Sets the `AUTH_KEY` environment variable to a new, randomly generated 32-character hex string (store a copy of this new key at `/app/new_auth_key.txt`).
   - Starts the SSH daemon on port 2222 (ensure sshd_config is configured to run as the local user and accepts the new key).
   - Starts the Python web server from the vendored package (`python /app/vendored_auth/secure-auth-server-1.2.0/server.py`) listening on `127.0.0.1:8080`.
   
Ensure both services remain running in the background when the script completes.