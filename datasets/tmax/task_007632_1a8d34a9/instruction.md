You are a penetration tester analyzing a simulated vulnerable application located at `/home/user/vuln_app/`.

Inside this directory, you will find:
1. `process_upload.sh`: A shell script that copies uploaded files into an `uploads/` directory. It contains a poorly implemented security filter intended to prevent path traversal attacks.
2. `db_dump.enc`: An AES-256-CBC encrypted database export containing sensitive user data. 

Your objective is to complete the following security tasks:

**Step 1: Exploit Crafting**
Analyze `process_upload.sh`. The script expects two arguments: an input file path and a target filename. Craft a payload string for the *target filename* (the second argument) that successfully bypasses the script's naive `../` check and would write a file directly to `/home/user/vuln_app/pwned.txt`. 
Write your exact payload string (and nothing else) into a new file at `/home/user/payload.txt`.

**Step 2: Decryption**
Decrypt the `/home/user/vuln_app/db_dump.enc` file. The encryption method used was `aes-256-cbc` with PBKDF2 (100000 iterations). 
The passphrase for the decryption is exactly the SHA-256 hash of the `process_upload.sh` file (just the 64-character lowercase hexadecimal string, no trailing filenames or spaces). 

**Step 3: Sensitive Data Redaction**
The decrypted database dump contains user names and credit card numbers. You must redact all 16-digit credit card numbers. 
- Credit cards may appear in either `1234123412341234` or `1234-1234-1234-1234` format.
- Replace every credit card number entirely with the exact string: `XXXX-XXXX-XXXX-XXXX`.
- Save the fully redacted output to `/home/user/redacted.txt`.

**Step 4: Cryptographic Verification**
Calculate the SHA-256 checksum of your final `/home/user/redacted.txt` file. Save the output of the `sha256sum` command exactly as it is formatted by default to `/home/user/hash.txt`.