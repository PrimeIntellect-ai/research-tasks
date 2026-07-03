You are acting as a security auditor tasked with securing a system where background processes have been found leaking credentials via command-line arguments (visible in `/proc`) and occasionally suffering from command injection vulnerabilities.

You must perform a multi-stage remediation and auditing workflow:

**Stage 1: Credential Recovery via OCR & Brute-force**
You have been provided with an image artifact at `/app/audit_policy.png`. This image contains a printed policy document that includes the SHA256 hash of the system's Audit Vault password. 
1. Use OCR tools (like `tesseract`, which is preinstalled) to extract the text from the image and find the hash.
2. The password is known to be a 4-digit PIN followed by the word "audit" (e.g., `1234audit`, `9999audit`). Write a Python script to brute-force this hash to discover the plaintext password.

**Stage 2: TLS Certificate Management for Sandboxing**
The audit logging mechanism requires a secure, sandboxed environment. 
1. Using the plaintext password recovered in Stage 1 as the key passphrase, generate a self-signed TLS/SSL certificate and private key.
2. Save the private key to `/home/user/audit_key.pem` and the certificate to `/home/user/audit_cert.pem`. Ensure the key is securely generated using RSA 2048-bit encryption.

**Stage 3: Command-Line Argument Classifier**
To prevent future credential leaks and command injection exploits, you must write a Python classifier that acts as a security filter.
1. Create a script at `/home/user/arg_classifier.py`.
2. The script must accept a single file path as a command-line argument. The file will contain a single simulated command-line invocation (e.g., `python worker.py --user admin --file logs.txt`).
3. Your script must analyze the command line and print EXACTLY the word `CLEAN` to standard output if the command is safe, or `EVIL` if it is malicious/insecure.
4. "EVIL" commands include:
   - Command injections (e.g., containing `;`, `&&`, `|`, `$()`, or backticks `\`` in argument values).
   - Credential leaks (e.g., passing `--password`, `--secret`, or `--token` followed by a cleartext value).
5. "CLEAN" commands are standard, safe invocations without sensitive flags or shell metacharacters.

Your classifier will be evaluated against a hidden corpus of clean and evil command invocations to ensure accurate detection without false positives.