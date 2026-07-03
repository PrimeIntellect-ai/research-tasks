You are a DevSecOps engineer enforcing security policies as code. 

We have a legacy deployment script located at `/home/user/deploy.py` that handles sensitive configurations. Currently, this script has several major security flaws:
1. It reads the decryption key directly from command-line arguments, which leaks the credential via process listings (`/proc/<pid>/cmdline`).
2. It decrypts a configuration file but does not verify its integrity.
3. It generates an HTML deployment report but fails to enforce a Content Security Policy (CSP).
4. It does not validate the TLS certificate used by the target deployment server.

Your task is to refactor the Python script `/home/user/deploy.py` to fix these issues. Modify the script to perform the following:

1. **Secure Key Loading:** Stop reading the key from `sys.argv`. Instead, read the decryption key from the file `/home/user/.secret_key`.
2. **Decryption and Integrity Check:** 
   - Use the loaded key (a valid Fernet key) to decrypt `/home/user/config.enc`.
   - Compute the SHA-256 hash of the decrypted plaintext (as UTF-8 bytes).
   - Read the expected hash from `/home/user/config.sha256`. 
   - If the computed hash does not perfectly match the expected hash string (lowercase hex), the script must exit immediately with status code 1.
3. **TLS Certificate Fingerprinting:**
   - Read the PEM-encoded certificate from `/home/user/server.crt`.
   - Extract its SHA-256 fingerprint (formatted as a hex string with colons, e.g., `01:23:45...`).
4. **Secure HTML Report Generation:**
   - If the integrity check passes, generate a report and save it to `/home/user/secure_report.html`.
   - The HTML file MUST contain a strict Content Security Policy meta tag exactly as follows:
     `<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'none';">`
   - The HTML body must contain the following three lines (separated by `<br>` or newlines):
     `Integrity: OK`
     `Cert Fingerprint: <your_computed_fingerprint>`
     `Config: <the_decrypted_plaintext>`

Do not change the name of the output report or the required formatting. You may use standard library modules and the `cryptography` package (which is already installed). When you are done, execute your refactored script (it should require no arguments) to generate the `/home/user/secure_report.html` file.