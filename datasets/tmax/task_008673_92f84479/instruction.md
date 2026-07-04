You are a forensics analyst investigating a compromised Linux host. You have recovered several artifacts left behind by the attacker in the `/home/user/forensics` directory. 

Your objective is to analyze the attacker's tools, mitigate the threat, redact stolen sensitive information, and document the evidence. 

Complete the following tasks:

1. **Code Auditing & CWE Identification**: 
   Analyze the recovered C source code `/home/user/forensics/attacker_tool.c`. The code contains a classic software vulnerability that allows a buffer overflow due to copying input without checking its length. Identify the specific MITRE CWE ID for this vulnerability (e.g., CWE-79, CWE-89). 
   Create a file at `/home/user/forensics/cwe_report.txt` containing exactly the CWE ID in the format:
   `CWE-XXX` (where XXX is the number).

2. **Network Policy Configuration**:
   The `attacker_tool.c` source code contains a hardcoded Command & Control (C2) IP address. Extract this IP address. Create a shell script at `/home/user/forensics/block_c2.sh` that contains a single `iptables` command to `DROP` all outbound (`OUTPUT`) traffic destined for this specific C2 IP address. 

3. **Sensitive Data Redaction**:
   The file `/home/user/forensics/stolen_data.txt` contains exfiltrated data, including highly sensitive Social Security Numbers (SSNs). 
   Write a C program at `/home/user/forensics/redact.c` that reads the contents of `stolen_data.txt` and replaces the last 4 digits of any SSN (format: `XXX-XX-XXXX`, where X is a digit) with the word `REDACTED` (resulting format: `XXX-XX-REDACTED`). 
   Compile your C program and run it to generate the cleaned output at `/home/user/forensics/redacted_data.txt`. Ensure all other text remains unmodified.

4. **Cryptographic Hashing**:
   Calculate the SHA-256 hash of the recovered binary payload `/home/user/forensics/malware_payload.bin`. 
   Save the result in `/home/user/forensics/hash_report.txt` in the exact format:
   `SHA256: <hash_value>`

Ensure all output files are placed exactly where requested with the precise formatting described.