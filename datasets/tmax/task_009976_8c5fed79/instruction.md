You are a security auditor hired to analyze a custom bash-based deployment system. The system is located at `/home/user/deploy_system`.

Your task is to perform an automated code and configuration audit of this directory using standard bash tools, focusing on file permissions, file integrity, and identifying a specific authentication bypass vulnerability.

Perform the following steps:

1. **Authentication Bypass Auditing:** The deployment system uses a custom token verification mechanism. Similar to the notorious "JWT alg=none" vulnerability, one of the bash scripts in the directory contains a logic flaw that explicitly permits authentication to succeed if the algorithm or token type is set to "none". Find this vulnerable script and identify the exact line of code that creates this bypass.

2. **Permissions Auditing:** Find all files (not directories) within `/home/user/deploy_system` (and its subdirectories) that are world-writable (i.e., write permission is granted to 'others'). 

3. **Certificate Integrity Verification:** The directory `/home/user/deploy_system/certs` contains several TLS certificate files (`*.pem`). There is a hash file at `/home/user/deploy_system/cert_hashes.sha256` containing the known-good SHA-256 hashes for these certificates. One of the certificates has been tampered with and no longer matches its expected hash. Identify the tampered certificate file.

Once you have completed your analysis, create an audit report at `/home/user/audit_report.txt` with exactly four lines in the following format:

Line 1: The base name of the bash script containing the auth bypass vulnerability (e.g., `script.sh`).
Line 2: The exact literal line of code from that script that contains the string "none" which facilitates the bypass (preserve exact spacing/quotes).
Line 3: A comma-separated list of the absolute paths of all world-writable files, sorted alphabetically (e.g., `/home/user/deploy_system/a.txt,/home/user/deploy_system/b/c.txt`).
Line 4: The base name of the tampered certificate file (e.g., `tampered.pem`).

Ensure your final output precisely matches this format so it can be automatically evaluated.