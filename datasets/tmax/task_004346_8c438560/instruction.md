You are a security engineer tasked with rotating credentials for a legacy authentication service and identifying past breaches. The previous maintainers left behind a compiled binary with a suspected hardcoded backdoor credential (violating CWE-259). Your goal is to reverse engineer the binary to find the credential, scan network logs to find attackers who exploited it, and implement a secure credential rotation mechanism in C++.

All files you need are in `/home/user/`.

**Phase 1: Binary Analysis & Reverse Engineering**
There is a stripped ELF binary located at `/home/user/legacy_auth`. It contains a hardcoded, obfuscated backdoor password in its `.rodata` section. The password is known to be obfuscated using a simple XOR cipher with the single-byte key `0x5A`.
1. Analyze the binary to locate and extract this obfuscated password.
2. Decrypt it and write the plaintext password to `/home/user/extracted_password.txt`. (Do not include any newlines or trailing spaces).

**Phase 2: Intrusion Detection (Pattern Matching)**
You have a binary network log file at `/home/user/traffic.bin`. The file consists of fixed-size 21-byte records representing authentication attempts:
- **Bytes 0-3:** Source IP address in network byte order (Big Endian).
- **Bytes 4-19:** The password attempt (16 bytes, null-padded ASCII).
- **Byte 20:** Success flag (1 byte, where `0x01` means successful login, `0x00` means failure).

1. Write a C++ program named `/home/user/detect_usage.cpp` that reads `/home/user/traffic.bin`.
2. The program must find all records where the password attempt matches the backdoor password you extracted in Phase 1 AND the success flag is `0x01`.
3. Compile and run your program so that it writes the compromised IP addresses (in standard dotted-decimal notation, e.g., `192.168.1.50`, one per line) to `/home/user/compromised_ips.txt`.

**Phase 3: Secure Credential Rotation**
To fix the CWE-259 vulnerability, we are moving to a securely hashed credential system. A new, strong plaintext password has been placed in `/home/user/new_password.txt`.
1. Write a C++ program named `/home/user/rotate.cpp` that reads the contents of `/home/user/new_password.txt`.
2. The program must compute the SHA-256 hash of this new password (you may use OpenSSL, which is installed on the system).
3. The program must write the resulting SHA-256 hash as a lowercase hexadecimal string to `/home/user/rotated_hash.txt` (without any trailing newline).
4. Compile your program to `/home/user/rotate` and execute it to generate the file. Link against the necessary crypto libraries (`-lcrypto`).

Complete all three phases to secure the system.