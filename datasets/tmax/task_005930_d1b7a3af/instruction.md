You are a security auditor hired to investigate a potential breach in a company's logging system. You have been granted access to the server. Your workspace is located at `/home/user/audit_system`. 

Inside this directory, you will find:
1. A `logs` directory containing several log files (`auth.log`, `system.log`, `access.log`).
2. A `hashes.txt` file containing the known-good SHA256 hashes of the log files before the suspected breach occurred. The format is `<sha256_hex> <filename>`.

Your audit requires you to perform the following steps:

**Phase 1: File Integrity Verification**
Write a C program at `/home/user/audit_system/verify_integrity.c` that reads the `hashes.txt` file, calculates the SHA256 hash of each corresponding file in the `/home/user/audit_system/logs/` directory, and compares the computed hash against the baseline. 
You may use the OpenSSL `libcrypto` library to calculate the hashes. If necessary, install any required development headers (you have passwordless sudo access).
Determine exactly one log file that has been tampered with (its hash will not match).

**Phase 2: Security Log Parsing**
The attacker attempted to brute-force the authentication service. Analyze `/home/user/audit_system/logs/auth.log`. Find the IP address that has the highest number of lines containing the exact string `FAILED LOGIN`. 

**Phase 3: Permission Auditing and Remediation**
The permissions on the log directory and its files have been misconfigured, leaving them globally writable. 
Remediate the permissions as follows:
- The `/home/user/audit_system/logs/` directory must have exact permissions `750`.
- All `.log` files within the directory must have exact permissions `640`.

**Phase 4: Reporting**
Generate a final report at `/home/user/audit_system/report.txt` containing exactly three lines:
Line 1: The exact filename (without the path) of the tampered log file (e.g., `access.log`).
Line 2: The IP address with the most `FAILED LOGIN` attempts.
Line 3: The word `REMEDIATED` to confirm you have fixed the permissions.

Ensure your C program compiles cleanly and that your report is strictly formatted as requested.