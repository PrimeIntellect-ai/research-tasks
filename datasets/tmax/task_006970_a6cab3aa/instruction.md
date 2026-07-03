You are a compliance analyst generating an audit trail for a security breach investigation. As part of the incident response process, you have been provided with an encrypted evidence archive containing the source code of the compromised application.

Your task is to analyze the codebase for specific vulnerabilities and generate an audit report.

1. Decrypt the evidence archive located at `/home/user/evidence.tar.enc`. It was encrypted using `openssl` with the `aes-256-cbc` cipher and PBKDF2 key derivation. The encryption password is `compliance2024`.
2. Extract the decrypted tarball into a new directory at `/home/user/src/`.
3. The extracted files contain the source code of a Rust application. Manually audit the Rust code or use pattern matching tools to identify exactly two critical security flaws:
   - An OS Command Injection vulnerability (CWE-78).
   - A Use of Hard-coded Password vulnerability (CWE-798).
4. Generate an audit report file at `/home/user/audit_report.txt`. The file must contain exactly two lines (sorted numerically by CWE ID) detailing the exact file name and line number where the vulnerabilities are located. Use the following format:
   `CWE-<ID>: <filename>:<line_number>`

Example of the expected `/home/user/audit_report.txt` format:
```
CWE-78: network.rs:42
CWE-798: database.rs:12
```

Note: The line number should correspond to the exact line where the vulnerable sink or hardcoded secret is declared.