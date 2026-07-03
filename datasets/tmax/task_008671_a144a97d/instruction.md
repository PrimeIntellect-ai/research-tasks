You are acting as a network security engineer investigating suspicious traffic. You have intercepted a payload and a custom authentication script used by a suspected threat actor. 

You have the following files in `/home/user/`:
1. `/home/user/auth_handler.py` - The authentication script intercepted from the network.
2. `/home/user/intercepted_hash.txt` - A text file containing a single MD5 hash captured during an authentication exchange.
3. `/home/user/payload.bin` - The binary payload whose integrity needs to be verified.

Your objectives are:
1. **Code Auditing & CWE Identification:** Analyze `auth_handler.py`. Identify the primary CWE (Common Weakness Enumeration) identifier specifically relating to the use of a cryptographically weak hashing algorithm.
2. **Password Cracking:** The intercepted hash corresponds to a 4-digit numeric PIN (0000-9999). Write a Python script to brute-force this PIN based on the hashing logic found in `auth_handler.py`.
3. **File Integrity Verification:** Calculate a keyed SHA-256 checksum of `/home/user/payload.bin` to create an integrity signature. The signature must be the SHA-256 hex digest of the cracked 4-digit PIN string immediately followed by the exact raw bytes of `payload.bin` (i.e., `sha256(PIN_string_bytes + payload_bytes)`).

You must output your findings to a file named `/home/user/investigation_report.txt` with exactly three lines in the following format:
Line 1: The exact CWE ID for the weak hashing algorithm (e.g., CWE-XXX).
Line 2: The cracked 4-digit PIN.
Line 3: The computed SHA-256 hex digest for the payload integrity verification.