You are a security auditor investigating a suspicious proprietary binary found on a compromised Linux workstation. 

You have been given a suspicious binary located at `/home/user/vuln_vault`. Preliminary analysis suggests this binary acts as a local credential vault and is protected by a 4-digit PIN (0000 to 9999). 

Your objective is to reverse engineer the binary's authentication mechanism, brute-force the PIN using a custom Rust application, extract the protected data, and secure the output file.

Perform the following steps:
1. **Analyze the ELF Binary:** Inspect `/home/user/vuln_vault` to extract the hardcoded MD5 hash used for PIN verification. The binary computes the MD5 hash of the user-provided 4-digit PIN concatenated with the salt string `AUDIT_SALT` (e.g., if the PIN is 1234, it hashes `1234AUDIT_SALT`). The expected 32-character hexadecimal MD5 hash is stored in plaintext within the binary's read-only data sections.
2. **Brute-Force the PIN:** Create a new Rust project in `/home/user/cracker` using `cargo`. Write a Rust program that iterates through all possible 4-digit PINs, concatenates each with `AUDIT_SALT`, computes the MD5 hash, and compares it against the extracted hash. You may use the `md-5` crate.
3. **Extract the Data:** Once you have the correct PIN, execute the binary passing the PIN and an output file path as arguments: 
   `/home/user/vuln_vault <PIN> /home/user/flag.txt`
   If the PIN is correct, the binary will write the decrypted secrets to `/home/user/flag.txt`.
4. **Secure the Output:** The binary writes the output file with insecure default permissions. As an auditor, you must strictly control access. Change the permissions of `/home/user/flag.txt` to strictly `0400` (read-only for the owner, no permissions for group or others).
5. **Generate Audit Report:** Write the cracked PIN to a log file located at `/home/user/audit_report.txt` with the exact format:
   `PIN: <the_4_digit_pin>`

Constraints:
- Do not attempt to modify the `vuln_vault` binary.
- Use Rust for the brute-forcing tool.
- Ensure the final permissions on `flag.txt` are exactly `-r--------`.