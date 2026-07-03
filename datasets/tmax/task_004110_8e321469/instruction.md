You are acting as a security engineer tasked with rotating credentials and auditing legacy weak hashes. We recently discovered that our hash auditing script (`/home/user/audit.py`) is extremely slow and also insecurely leaks the password wordlist via command-line arguments (which are visible to all users via `/proc`).

Your objectives are:

1. **Fix the Performance Bottleneck in the Vendored Cryptography Library:**
   We use a custom-vendored version of `passlib` (version 1.7.4) located at `/app/passlib-1.7.4`. A junior developer previously tampered with the MD5-crypt handler for "rate limiting" purposes, but it severely impacts our auditing throughput.
   - Inspect the `passlib` source code in `/app/passlib-1.7.4`.
   - Locate and remove the artificial performance penalty (a `time.sleep` call) injected into the `md5_crypt` implementation.
   - Install this patched version of the library into the system Python environment.

2. **Secure the Audit Script:**
   The current script `/home/user/audit.py` receives a comma-separated list of candidate passwords via a CLI argument (`--passwords`). 
   - Modify `/home/user/audit.py` so that it no longer accepts passwords via CLI arguments.
   - Instead, it must read the candidate passwords from a file `/home/user/wordlist.txt` (one password per line).
   - Ensure the modified script still verifies the hashes listed in `/home/user/legacy_hashes.txt` against the wordlist.

3. **Generate the Audit Output:**
   - Create the `/home/user/wordlist.txt` file using a dictionary of common passwords (e.g., "password", "123456", "admin", "secret", "qwerty").
   - Run your modified `/home/user/audit.py`.
   - The script must successfully crack the hashes and output a JSON file at `/home/user/cracked.json` containing a dictionary mapping the original hash strings to their cracked plaintext passwords.

The automated verification will check the structure of `/home/user/cracked.json`, ensure no passwords are leaked via `/proc` command-line arguments during execution, and rigorously benchmark the MD5-crypt verification speedup.