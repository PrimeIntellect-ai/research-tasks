You are a security engineer responding to a security incident involving a legacy authentication service. You need to perform a series of credential rotations, vulnerability remediations, and cryptographic verifications.

All your work will take place in `/home/user/incident_response/`.

Here are your tasks:

**Phase 1: Password Cracking & Credential Rotation**
An attacker leaked a file containing password hashes of our administrators at `/home/user/incident_response/admin_hashes.txt`. The format is `username:sha256_hash`.
You have been provided a company wordlist at `/home/user/incident_response/wordlist.txt`.
1. Crack the hashes to determine the compromised passwords.
2. Write the cracked credentials to `/home/user/incident_response/cracked_passwords.json` in the exact format: `{"username": "plaintext_password"}`.

**Phase 2: Vulnerability Remediation**
The leaked credentials allowed attackers to exploit the internal login service located at `/home/user/incident_response/auth_service/app.py` (a Python Flask application).
The application currently suffers from two vulnerabilities:
1. **SQL Injection:** The `login()` function constructs SQL queries insecurely.
2. **Open Redirect:** The login flow redirects users to the `next` parameter without validation.
Your task is to patch `/home/user/incident_response/auth_service/app.py`. Modify the code to use parameterized SQL queries (using sqlite3) and ensure the `next` parameter only allows relative paths (must start with `/` and not contain `//` or absolute URLs). Do not change the function signatures or the database schema.

**Phase 3: Cryptographic Token Rotation**
The service stores an encrypted master token in `/home/user/incident_response/tokens/master_token.enc`. It was encrypted using AES-256-CBC with the key stored in `/home/user/incident_response/keys/old_key.bin` and the IV stored in `/home/user/incident_response/keys/old_iv.bin`.
1. Decrypt the master token.
2. Re-encrypt the plaintext token using AES-256-CBC with the new key (`/home/user/incident_response/keys/new_key.bin`) and new IV (`/home/user/incident_response/keys/new_iv.bin`).
3. Save the newly encrypted token to `/home/user/incident_response/tokens/master_token_rotated.enc`.

**Phase 4: Certificate Chain Validation**
The service communicates with an upstream provider. The certificate chain provided by the upstream is located at `/home/user/incident_response/certs/chain.pem`, and our trusted root CA is at `/home/user/incident_response/certs/rootCA.pem`.
One of the intermediate certificates in the chain is invalid (e.g., expired or wrong signature).
1. Analyze the chain.
2. Extract the Subject Common Name (CN) of the invalid/failing certificate.
3. Write just the Common Name string to `/home/user/incident_response/invalid_cert_cn.txt` (e.g., if the subject is `CN = Bad-Intermediate-CA`, write `Bad-Intermediate-CA`).

Ensure all output files are placed exactly where specified with the correct formats.