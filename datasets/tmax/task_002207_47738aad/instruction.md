You are acting as a penetration tester auditing a compromised local service. In the directory `/home/user/pentest_audit`, you will find two files:
1. `vuln_auth.cpp` - The source code for the local authentication service.
2. `network_logs.txt` - A log of recent authentication attempts.

Your task consists of four parts:

**Part 1: Code Auditing (CWE Identification)**
Audit `vuln_auth.cpp`. The developer used a custom, weak hashing algorithm and hardcoded the expected admin hash directly in the source code. Identify the primary CWE (Common Weakness Enumeration) identifier for the vulnerability "Use of Hard-coded Credentials".
Write the exact CWE ID (format: `CWE-XXX`) to a file named `/home/user/pentest_audit/cwe_report.txt`.

**Part 2: Password Cracking (C++)**
The hardcoded admin hash in `vuln_auth.cpp` corresponds to a 4-digit numeric PIN (0000-9999). 
Write a C++ program in `/home/user/pentest_audit/cracker.cpp` that brute-forces this custom hash function to find the original 4-digit PIN. Compile and run it.
Save the cracked 4-digit PIN to `/home/user/pentest_audit/cracked_pin.txt`.

**Part 3: Data Redaction**
The file `network_logs.txt` contains plain-text authentication attempts, including PINs. Process this file to redact all sensitive PINs.
Replace any 4-digit number following `PIN=` with `XXXX`. 
Save the completely redacted log to `/home/user/pentest_audit/redacted_logs.txt`. 

**Part 4: Firewall Configuration Generation**
Analyze the original `network_logs.txt`. Identify the IP address that attempted to log in (and failed) more than 3 times. 
Generate a bash script at `/home/user/pentest_audit/firewall_rule.sh` containing a single `iptables` command to append a rule dropping all incoming traffic (`INPUT` chain) from that specific IP address. Ensure the script is executable.

You must rely on your C++ and bash skills. Output only the requested files.