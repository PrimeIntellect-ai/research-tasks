You are a DevSecOps engineer responsible for enforcing policy-as-code and remediating vulnerabilities in legacy system components. 

During a recent security audit, you identified a critical flaw in a legacy configuration parser written in C. This tool reads proprietary configuration files but lacks basic security controls. 

Your task is to demonstrate the vulnerability, prove the weakness of the existing authentication policy, fix the code, and enforce strict data redaction policies.

You must complete the following phases:

**Phase 1: Password Cracking (Policy Audit)**
The legacy system stores a weakly hashed 4-digit PIN that restricts access to certain configuration nodes. The MD5 hash of this 4-digit PIN is stored in `/home/user/pin_hash.txt`. 
1. Determine the original 4-digit PIN.
2. Save the cracked 4-digit PIN to `/home/user/cracked_pin.txt` (the file should contain only the 4 digits and nothing else).

**Phase 2: Exploit Crafting (Vulnerability Proof-of-Concept)**
The parser binary is located at `/home/user/legacy_parser` (source code is at `/home/user/legacy_parser.c`). It contains a buffer overflow vulnerability.
1. Write a Python script at `/home/user/exploit.py` that, when executed, generates a payload file named `/home/user/malicious.cfg`.
2. The payload must exploit the buffer overflow in `legacy_parser` such that running `/home/user/legacy_parser /home/user/malicious.cfg` outputs EXACTLY the string `POLICY_VIOLATION_TRIGGERED`. 
*(Note: Do not rely on ASLR bypasses or shellcode; simply overwrite the adjacent logical control variable `admin_priv` in the binary's struct).*

**Phase 3: Secure Coding & Sensitive Data Redaction**
You must fix the C source code to meet modern DevSecOps standards.
Modify `/home/user/legacy_parser.c` to accomplish the following:
1. **Fix the Vulnerability:** Prevent the buffer overflow (ensure the buffer cannot be overflowed, e.g., by bounding the read operation to 63 characters).
2. **Implement Redaction:** Add a redaction routine. Before printing the "Config loaded: ..." message, the program must scan the parsed string. If it finds the sequence `PIN=` followed exactly by four digits (e.g., `PIN=1234`), it must replace those four digits with asterisks (`PIN=****`). It should handle any 4 digits.
3. Compile your fixed version using the command: `gcc -O0 -o /home/user/secure_parser /home/user/legacy_parser.c`.

**Phase 4: File Integrity Verification**
As part of the deployment pipeline, a cryptographic hash of the compiled secure binary must be logged.
1. Generate a SHA-256 checksum of the newly compiled `/home/user/secure_parser`.
2. Save the output in the standard `sha256sum` format to `/home/user/secure_parser.sha256`.

**Constraint Checklist & Confidence Score:**
- `cracked_pin.txt` contains the correct 4 digits?
- `exploit.py` generates `malicious.cfg`?
- `legacy_parser malicious.cfg` triggers the violation?
- `secure_parser` is compiled and safe from the overflow?
- `secure_parser` correctly redact the PIN data in its stdout?
- `secure_parser.sha256` contains the valid SHA-256 hash?