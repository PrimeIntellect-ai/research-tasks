You are a penetration tester analyzing a compromised system. You have found a custom data processing application written in C++ that the system uses to parse logs before transferring them. 

You need to perform a security audit on this tool, patch it, run it safely, and prepare a hardened SSH configuration for secure data transfer.

Perform the following steps:

1. **Binary Analysis (ELF):**
   Analyze the compiled binary located at `/home/user/processor.elf`. There is a hardcoded 32-character hexadecimal token embedded in the `.rodata` section, prefixed with the string `SECRET_TOKEN:`. Extract the 32-character hex token and save it to `/home/user/token.txt` (just the 32 characters, no newline, no prefix).

2. **CWE Identification & Patching:**
   The source code for the processor is in `/home/user/src/main.cpp`. It contains a classic Buffer Overflow vulnerability (CWE-120/CWE-119) in the `process_line` function, which uses an unsafe C-string copy mechanism into a fixed-size 128-byte buffer. 
   Rewrite the `process_line` function to use safe C++ `std::string` operations, completely removing the fixed-size buffer vulnerability. 

3. **Sensitive Data Redaction:**
   While editing `/home/user/src/main.cpp`, add redaction logic inside `process_line` before the line is returned.
   - Find all standard 9-digit US Social Security Numbers formatted as `XXX-XX-XXXX` and replace them exactly with `***-**-****`.
   - Find all 16-digit credit card numbers (contiguous digits, e.g., `1234567890123456`) and replace the first 12 digits with asterisks, leaving the last 4 digits visible (e.g., `************3456`).
   
4. **Compilation and Execution:**
   Compile your patched source code:
   `g++ -O2 -std=c++11 /home/user/src/main.cpp -o /home/user/patched_processor`
   Run it on the raw log file:
   `/home/user/patched_processor /home/user/raw.log /home/user/clean.log`

5. **SSH Hardening:**
   Create an unprivileged, hardened SSH server configuration file at `/home/user/sshd_config`. This file will be used to run a local SSH daemon securely to transfer the logs. It must contain EXACTLY these directives (along with any required paths for host keys, which you can set to `/home/user/ssh_host_rsa_key`):
   - Listen on Port `2222`
   - Disable `PasswordAuthentication`
   - Disable `X11Forwarding`
   - Disable `PermitRootLogin`
   - Only allow the user `user` (`AllowUsers user`)
   - Restrict the MACs algorithm to `hmac-sha2-256`

Ensure all output files (`token.txt`, `clean.log`, `sshd_config`) are in the exact locations specified.