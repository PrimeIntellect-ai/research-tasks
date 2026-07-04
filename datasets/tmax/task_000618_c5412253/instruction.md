You are acting as a DevSecOps engineer enforcing policy as code. A developer has submitted a custom C-based authentication module, along with an encrypted audit log, for a security review before deployment. 

Your objective is to audit the code, break the weak encryption to verify its contents, and extract a sensitive deployment token.

Perform the following tasks:

1. **Automated Vulnerability Scanning (Pattern Matching)**
   Review the source code located at `/home/user/project/auth_module.c`. You must identify all instances of the banned unsafe C functions: `gets`, `strcpy`, and `sprintf`.
   Create a vulnerability report at `/home/user/vuln_report.txt`. Each line must contain the exact line number and the banned function found, in the following format:
   `[Line Number]: [Function]`
   (Example: `12: strcpy`)
   Order the report by line number in ascending order.

2. **Password Cracking & Decryption**
   The developer encrypted the audit log located at `/home/user/project/audit_log.enc` using a weak custom XOR cipher. 
   - The cipher simply XORs the plaintext with a repeating key.
   - The key is exactly 4 characters long and consists entirely of lowercase English letters (`a-z`).
   - You know that the unencrypted log file begins exactly with the string: `SECURE_LOG_V1`
   
   Write and execute a C program to brute-force the 4-character key. Once you discover the key, decrypt the entire file and save the plaintext output to `/home/user/audit_log.dec`.

3. **Intrusion/Secrets Detection**
   Inspect the decrypted log file (`/home/user/audit_log.dec`). It contains a leaked deployment token matching the pattern `TOKEN-` followed by 16 uppercase alphanumeric characters.
   Extract just the token string (e.g., `TOKEN-A1B2C3D4E5F6G7H8`) and write it to `/home/user/token.txt` with no trailing newline.

Ensure all output files (`vuln_report.txt`, `audit_log.dec`, `token.txt`) are placed directly in `/home/user/`.