You are a forensics analyst recovering evidence from a compromised Linux host. The attacker managed to exploit a vulnerability, exfiltrate data, and obfuscate it. You need to use your Bash scripting skills to analyze the intrusion and recover the exfiltrated data. 

All your work must be done using pure Bash, shell built-ins, and standard Linux coreutils (`awk`, `sed`, `grep`, `xxd`, `tr`, etc.). Do not use scripting languages like Python, Perl, or Ruby.

**Phase 1: Intrusion Detection**
1. An access log has been captured at `/home/user/evidence/server.log`.
2. Parse this log to identify the attacker's IP address. The attacker successfully executed an SQL injection attack (identified by the string `UNION SELECT` in the HTTP request that resulted in a successful `200` HTTP status code).
3. Extract only the attacker's IP address and save it to a file exactly at `/home/user/attacker_ip.txt`.

**Phase 2: Cryptanalysis and Data Recovery**
1. The attacker left an obfuscated exfiltration payload at `/home/user/evidence/blob.hex`. The file contains a single continuous string of hex characters.
2. Forensic intelligence suggests the payload was encrypted using a single-byte XOR cipher before being hex-encoded. 
3. Write a Bash script to perform an automated brute-force cryptanalysis against the hex blob, testing all possible 256 single-byte keys (0x00 through 0xFF). 
4. We know the decrypted plaintext contains the exact string `FLAG{`. 
5. Once you successfully decrypt the payload and find the plaintext containing the flag, extract ONLY the flag (the string starting with `FLAG{` and ending with `}`) and save it to `/home/user/flag.txt`.

Ensure your final output files (`/home/user/attacker_ip.txt` and `/home/user/flag.txt`) contain no extra spaces or newlines other than the required values.