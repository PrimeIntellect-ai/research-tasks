You are a DevSecOps engineer enforcing policy-as-code on a legacy application system. 

We have an old compiled binary located at `/home/user/vulnerable_backend`. We have lost its source code, but we know it performs an XOR-based encryption on sensitive data using a single-byte hardcoded key. 

An encrypted export from this backend has been saved to `/home/user/encrypted.dat`. This data contains sensitive Social Security Numbers (SSNs) and lacks modern web protections.

Your task is to create a secure C program `/home/user/secure_processor.c` that securely processes this data. Your program must perform the following:

1. **Reverse Engineering & Decryption**: Analyze `/home/user/vulnerable_backend` to find the single-byte XOR key. Your C program must use this key to decrypt the contents of `/home/user/encrypted.dat`.
2. **Process Isolation (Sandboxing)**: To prevent any potential vulnerability in the parsing logic from being exploited, your program MUST restrict its own privileges using strict seccomp. Specifically, immediately after opening the required input and output files, you must call `prctl(PR_SET_SECCOMP, SECCOMP_MODE_STRICT)`. You may not perform any system calls other than `read`, `write`, `_exit`, and `sigreturn` after this point.
3. **Content Security Policy Enforcement**: Prepend the exact string `Content-Security-Policy: default-src 'none';\n\n` to the beginning of the final output.
4. **Sensitive Data Redaction**: The decrypted text will contain SSNs in the format `XXX-XX-XXXX` (where X is a digit). You must redact these by replacing every digit in the SSN with an asterisk `*`, resulting in `***-**-****`. The rest of the text must remain unchanged.

**Execution & Verification**:
- Your program must read `/home/user/encrypted.dat` and write the final secured, decrypted, and redacted output to `/home/user/redacted.txt`.
- Compile your program to `/home/user/secure_processor` (e.g., `gcc -o /home/user/secure_processor /home/user/secure_processor.c`).
- Run `/home/user/secure_processor` so that `/home/user/redacted.txt` is successfully generated.

Ensure your code safely manages file descriptors and buffers so that it does not crash under the strict seccomp policy.