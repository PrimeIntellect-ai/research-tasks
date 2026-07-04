As a DevSecOps engineer, you are tasked with implementing a "policy as code" auditing tool in C. You need to write a C program that performs a local security audit covering SSH configuration, TLS certificate validity, and basic intrusion detection from logs.

Write a C program at `/home/user/sec_audit.c` and compile it to `/home/user/sec_audit`. When executed, the program must evaluate three things and write a report to `/home/user/audit_report.txt`.

The program must perform the following checks:

1. **SSH Hardening Check:**
   Parse the SSH configuration file located at `/home/user/sshd_config`. 
   The configuration is considered hardened ONLY if it contains the exact active (uncommented) lines `PermitRootLogin no` and `PubkeyAuthentication yes`. If either is missing, commented out, or has a different value, the SSH configuration is NOT hardened.

2. **Certificate Validation:**
   Verify the TLS certificate chain. You are provided a certificate authority file at `/home/user/ca.pem` and a server certificate at `/home/user/server.pem`. 
   You must determine if `server.pem` is properly signed by `ca.pem`. You may invoke standard OpenSSL command-line tools from within your C program (e.g., using `popen` or `system`) to perform this check.

3. **Intrusion Detection (Pattern Matching):**
   Parse the authentication log file located at `/home/user/auth.log`. 
   Identify any IP addresses that have 3 or more "Failed password" attempts. A standard log entry looks like: `Failed password for invalid user admin from 10.9.8.7 port ...` or `Failed password for root from 192.168.1.5 port ...`. 
   Extract the IPv4 addresses and count their occurrences.

**Output Format:**
Your C program must create or overwrite `/home/user/audit_report.txt` with exactly the following format:
```
SSH_HARDENED: [YES/NO]
CERT_VALID: [YES/NO]
MALICIOUS_IPS: [comma-separated list of IPs with >= 3 failures, sorted alphabetically by string, or NONE if no IPs meet the threshold]
```

Example output:
```
SSH_HARDENED: NO
CERT_VALID: YES
MALICIOUS_IPS: 10.0.0.5, 192.168.1.100
```

Constraints:
- You must write the solution primarily in C (`/home/user/sec_audit.c`).
- Ensure the output strictly matches the requested format.
- Do not require root privileges to run your program.