You are a forensics analyst investigating a compromised Linux host. The attacker left behind a custom authentication binary, `/home/user/forensics/auth_vault`, along with its source code `/home/user/forensics/auth_vault.c`. We suspect this binary is used to lock stolen evidence, and we need to recover the hidden data.

Your objectives:
1. **Password Cracking:** The binary expects a 5-digit numerical PIN. Analyze the `auth_vault.c` source code to understand the custom hashing algorithm. Identify the hardcoded target hash and crack the 5-digit PIN using a brute-force approach.
2. **Code Auditing & Exploit Crafting:** Even with the correct PIN, the binary does not normally output the stolen evidence. However, auditing the source code reveals a memory corruption vulnerability (CWE-120) in the logging mechanism when a successful authentication occurs. 
3. **Evidence Extraction:** Craft an exploit payload to hijack the execution flow of the binary and force it to execute the hidden `secret_recovery()` function. Execute the binary with your exploit to retrieve the hidden evidence flag.
4. **Cryptographic Verification:** Compute the SHA-256 hash of the recovered flag string (excluding any trailing newlines).

You must write your findings to a precise log file at `/home/user/forensics/recovery_report.txt` with the following format:
```
PIN: [The 5-digit cracked PIN]
FLAG: [The exact evidence flag recovered from the binary]
FLAG_SHA256: [The SHA-256 hash of the flag]
```

Constraints & Environment:
* All files are located in `/home/user/forensics/`.
* The binary is already compiled with standard memory protections disabled for the vulnerable function (`-fno-stack-protector -no-pie`) to simulate an older legacy system the attacker targeted. 
* Standard Linux CLI tools, GCC, and scripting languages (like Python or Perl) are available for crafting payloads and cracking the PIN.