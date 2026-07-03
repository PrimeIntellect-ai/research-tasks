You are a DevSecOps engineer tasked with implementing a local "policy-as-code" enforcement tool in C.

Your task has two phases:

**Phase 1: TLS Certificate Management**
Write a bash script at `/home/user/gen_certs.sh` that uses `openssl` to generate a self-signed TLS certificate and private key.
- The output files must be `/home/user/certs/server.crt` and `/home/user/certs/server.key`.
- Key specs: RSA 2048-bit.
- Validity: Exactly 30 days.
- Subject: The Common Name (CN) must be `policy.local`.
- Ensure the `/home/user/certs/` directory exists.
Execute the script to create the certificates.

**Phase 2: The Policy Auditor (C Program)**
Write a C program at `/home/user/auditor.c` that performs the following security audits and actions:

1. **Sensitive Data Redaction:**
   Read the log file located at `/home/user/data/transactions.log`. Detect any contiguous sequence of exactly 16 digits (e.g., credit card numbers) and redact them by replacing each digit with the `*` character (exactly 16 asterisks). Write the fully redacted log to `/home/user/data/transactions_clean.log`.

2. **Privilege Escalation Auditing:**
   Scan the directory `/home/user/jail/bin` (non-recursive) for any files that have the SUID (Set-User-ID) bit enabled.

3. **Service Auditing:**
   Read the file `/home/user/data/open_ports.txt`, which contains one integer port number per line representing currently listening TCP ports. The only allowed ports are `22` and `443`. Any other port is considered unauthorized.

4. **Reporting:**
   The C program must output a JSON report to `/home/user/audit.json` formatted exactly like this (ensure proper JSON syntax, spaces, and sorted arrays):
   ```json
   {
     "suid_files": [
       "/home/user/jail/bin/bad_suid",
       "/home/user/jail/bin/root_shell"
     ],
     "unauthorized_ports": [
       80,
       3306
     ]
   }
   ```
   *Note: Both the `suid_files` array (alphabetically) and the `unauthorized_ports` array (numerically) must be sorted in ascending order.*

Compile your C program to `/home/user/auditor` and execute it to produce the redacted log and the JSON report. Ensure all required files and the JSON report are correctly generated.