You are a forensics analyst investigating a compromised Linux host. The attacker managed to persist access by modifying SSH configurations and left behind a suspicious encoded payload. 

Your objective is to identify the unauthorized access method, decode the payload, and extract the malicious indicator based on a strict security policy.

Here is what you need to do:

1. **File Integrity & SSH Hardening:**
   The file `/home/user/.ssh/authorized_keys` contains several SSH public keys. A list of known, authorized keys is located at `/home/user/evidence/valid_keys.pub`. 
   Identify the rogue SSH key that was added by the attacker. Obtain the MD5 fingerprint of this rogue key (e.g., `MD5:xx:xx:xx...`).

2. **Payload Decoding & Policy Enforcement:**
   The file `/home/user/evidence/payload.b64` contains a base64-encoded string left by the attacker. 
   Write a Python script `/home/user/analyze.py` that reads this file, decodes the base64 string, and parses the resulting comma-separated list of URLs. 
   Apply a simple Content Security Policy: identify the single URL in the list that violates the rule "No domains ending in .xyz or .ru are permitted". 

3. **Reporting:**
   Create a report file at `/home/user/forensics_report.txt` with exactly two lines:
   - Line 1: The MD5 fingerprint of the rogue SSH key (format: `2048 MD5:ab:cd:... attacker@evil (RSA)` or however `ssh-keygen` outputs it, just paste the exact output string of `ssh-keygen -l -E md5 -f <rogue_key_file>`).
   - Line 2: The exact malicious URL extracted from the decoded payload.

Note: You can use any combination of shell commands and Python code to accomplish this. Python 3 is available on the system.