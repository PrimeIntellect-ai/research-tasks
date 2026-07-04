You are a security engineer responsible for rotating credentials for a legacy internal service. As part of the rotation process, you need to perform a security audit, recover a weakly encrypted legacy key, and validate the new certificate chain.

Complete the following three tasks in your terminal:

1. **Cryptanalysis of Legacy Token:**
   The old authentication system used a weak custom cipher (a repeating 4-byte XOR key). We have intercepted an old token at `/home/user/legacy_token.bin`. We know the exact plaintext for this token is:
   `{"user":"admin","action":"rotate"}`
   Write a Python script to recover the 4-byte XOR key. Write the recovered key as an 8-character hexadecimal string to `/home/user/recovered_key.txt`.

2. **Privilege Escalation Audit:**
   The automated scripts used for credential rotation are stored in `/home/user/rotation_scripts/`. An automated cron job runs these scripts as a highly privileged service account. One of the Python scripts in this directory has insecure file permissions (world-writable), which poses a severe local privilege escalation risk.
   Identify the vulnerable file, change its permissions to `755`, and write the base filename (e.g., `vulnerable.py`) to `/home/user/vuln_file.txt`.

3. **Certificate Chain Validation:**
   The new service credentials rely on an updated PKI. The certificates are located in `/home/user/certs/`:
   - `/home/user/certs/ca.crt` (Root CA)
   - `/home/user/certs/intermediate.crt` (Intermediate CA)
   - `/home/user/certs/server.crt` (Leaf Certificate)
   
   Write a Python script at `/home/user/check_certs.py` that programmatically verifies the certificate chain (ensuring `server.crt` is valid and chains up to `ca.crt` via `intermediate.crt`). You may use the `cryptography` Python library or wrap the `openssl` command line tool using Python's `subprocess` module.
   If the chain is valid, the Python script must write the exact string `CHAIN_OK` to `/home/user/chain_status.txt`. Run your script to produce this file.

Ensure all output files (`recovered_key.txt`, `vuln_file.txt`, `chain_status.txt`) are created with the exact requested contents.