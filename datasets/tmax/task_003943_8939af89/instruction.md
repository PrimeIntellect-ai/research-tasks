You are a security auditor reviewing a legacy internal log-viewer application. The application environment is partially broken, and the legacy access control binary needs to be replaced with a transparent Python script. 

Your task is divided into three parts: Infrastructure Setup, Service Composition, and Validator Reimplementation.

**Part 1: SSH Hardening & Setup**
The backend service relies on SSH to read local logs securely.
1. Generate an `ed25519` SSH keypair for the user `user` without a passphrase. Save it to `/home/user/.ssh/id_ed25519`.
2. Append the public key to `/home/user/.ssh/authorized_keys`. To harden the configuration, prefix the key in `authorized_keys` with `restrict,command="/usr/bin/tail -n 50 /var/log/syslog" ` so it can only perform this action.
3. Edit the backend configuration file at `/app/config.json`. Change the `"ssh_key_path"` value to point to your newly created private key (`/home/user/.ssh/id_ed25519`).

**Part 2: Service Composition**
The application consists of Nginx, a Flask backend, and a Redis caching server.
1. Redis is installed. Ensure `redis-server` is running on its default port (6379).
2. Edit `/app/nginx.conf`. Configure the server block listening on port 8080 to proxy requests from `/` to the Flask backend at `http://127.0.0.1:5000`. You must also ensure Nginx injects the HTTP header `X-Auditor-Check: active` into the proxied request.
3. Start Nginx using this configuration file: `nginx -c /app/nginx.conf`.
4. Start the Flask application by running `python3 /app/app.py &`.
5. Ensure the entire pipeline works by using `curl -H "Cookie: session=test" http://127.0.0.1:8080/`. It should return a successful JSON response.

**Part 3: Validator Reimplementation (Algorithmic Equivalence)**
The system currently uses an obfuscated compiled binary located at `/app/oracle_validator` to validate requests. You must write a bit-exact equivalent Python replacement at `/home/user/validator.py`.

The script must accept exactly two command-line arguments:
`python3 /home/user/validator.py <cookie_value> <log_line>`

The logic for the validator is as follows:
1. **Intrusion Detection:** Apply a case-insensitive regex pattern match to `<log_line>`. If the line contains any of the following patterns, it is an intrusion attempt:
   - `union select` (with any amount of whitespace between the two words)
   - `/etc/shadow`
   - `<script>`
   If an intrusion pattern is found, print exactly `DENY_IDS` to stdout and exit.
2. **Cookie Validation (Password Cracking):** The system prefixes the `<cookie_value>` with a secret 4-digit PIN and computes the SHA-256 hash of the resulting string (e.g., `SHA256("1234mycookie")`).
   - We do not know the PIN, but we recovered a known valid combination: when the cookie was `"admin_token_99"`, the SHA-256 hash was `c5e5ba814d4a8e0f6f0c78aee35dcffb44fb7b35520a4be59c3a2f8c5b96bf28`.
   - Your script must systematically crack this 4-digit PIN (brute-force 0000-9999) using the known hash during its execution (or you can crack it beforehand and hardcode it).
   - Once the PIN is known, compute the SHA-256 hash of the PIN concatenated with the provided `<cookie_value>` argument. 
3. **Final Decision:** If the resulting hexadecimal hash ends with the character `a`, `b`, or `c`, print `ALLOW`. Otherwise, print `DENY_AUTH`.

Ensure your script `/home/user/validator.py` has a shebang `#!/usr/bin/env python3` and is executable (`chmod +x`).