You are a DevSecOps engineer tasked with remediating a critical security incident and enforcing policy as code to prevent future occurrences. 

An old deployment mechanism leaked sensitive deployment PINs via process command-line arguments, which were captured in our execution audit logs. Furthermore, several deployment scripts in our repository are suspected of containing similar hardcoded secrets passed as command-line arguments.

Your objective has three phases:

**Phase 1: Log Parsing & Brute-Force**
1. Read the process execution log located at `/home/user/logs/process_exec.log`.
2. Identify the leaked MD5 hash of the 4-digit numeric deployment PIN passed to the `--pin-hash` argument.
3. Write a Python script to crack this MD5 hash (it is exactly 4 digits, e.g., 0000 to 9999).

**Phase 2: Certificate Management**
The cracked 4-digit PIN is the passphrase for an encrypted private key located at `/home/user/certs/encrypted_app.key`.
1. Decrypt the private key and save it as `/home/user/certs/decrypted_app.key` (without a passphrase).
2. Generate a new self-signed X.509 certificate using the decrypted key. The certificate must be saved at `/home/user/certs/app.crt`.
3. The certificate must have a validity of exactly 365 days and the Subject Common Name (CN) must be `secure.local`.

**Phase 3: Policy as Code (Vulnerability Scanning)**
To prevent future leaks, write a custom Python scanner `/home/user/scan_leaks.py` that scans all `.sh` files in `/home/user/scripts/`.
1. The scanner should look for any line containing the exact string `--password=` or `-p ` followed by a string of non-whitespace characters.
2. The scanner must extract the leaked password value for each occurrence.
3. The scanner must output a JSON report to `/home/user/leak_report.json` with the following exact format:
```json
{
  "leaks": [
    {
      "file": "/home/user/scripts/example.sh",
      "line_number": 5,
      "leaked_password": "extracted_value"
    }
  ]
}
```
(Sort the list by `file` name, then `line_number` ascending).

Execute your scanner to generate the `/home/user/leak_report.json` file. Ensure all output files (`decrypted_app.key`, `app.crt`, and `leak_report.json`) are correctly formatted and placed in the specified directories.