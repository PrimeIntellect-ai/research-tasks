You are a compliance analyst tasked with generating audit trails for an old proprietary logging daemon while simultaneously identifying its vulnerabilities and developing a temporary mitigation until the vendor provides a patch.

You have been provided with the source code for the daemon at `/home/user/legacy_auditd.c`. 

Your objectives are to complete the following multi-phase task:

**Phase 1: Exploit Crafting (Vulnerability Proof-of-Concept)**
The `legacy_auditd.c` daemon contains a buffer overflow vulnerability. When compiled with ASLR disabled, it is susceptible to a return address overwrite.
1. Compile the daemon using: `gcc -O0 -fno-stack-protector -no-pie -o /home/user/legacy_auditd /home/user/legacy_auditd.c`
2. Write an exploit generator (in C, Bash, or Python) that creates a payload file at `/home/user/payload.bin`. 
3. Run the daemon using `setarch $(uname -m) -R /home/user/legacy_auditd < /home/user/payload.bin`.
4. Your payload must exploit the buffer overflow to redirect execution to the hidden `compliance_flag_reached()` function within the binary. When successfully executed, this function will create a file at `/home/user/audit_flag.txt`.

**Phase 2: Audit Trail Encryption**
For compliance reasons, the generated audit flag must be securely encrypted before transmission.
1. Encrypt `/home/user/audit_flag.txt` using AES-256-CBC.
2. Use the exact 256-bit Key: `0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef` (hex)
3. Use the exact 128-bit IV: `00112233445566778899aabbccddeeff` (hex)
4. Save the encrypted binary output to `/home/user/audit_trail.enc`.

**Phase 3: Security Policy Enforcement (Sandbox)**
To prevent potential network exfiltration if the vulnerability is exploited in the wild, you must create a mandatory security policy.
1. Write a C program at `/home/user/sandbox.c`.
2. This program must use `libseccomp` to enforce a strict system call filter. 
3. The filter must ALLOW all default system calls, but explicitly BLOCK the `socket` system call (kill the process or return an error if it is called).
4. After applying the filter, your sandbox program should execute the daemon using `execv("/home/user/legacy_auditd", args)`.
5. Compile your sandbox to `/home/user/sandbox` (you may need to install `libseccomp-dev` via your package manager, e.g., `sudo apt-get install -y libseccomp-dev` or similar if you have privileges, but assume you have standard access. If `libseccomp-dev` is missing, use `sudo apt-get update && sudo apt-get install -y libseccomp-dev`). *Note: sudo without password is configured for this container.*

**Constraints and Verification:**
- Do not modify `legacy_auditd.c`.
- The final encrypted file must be located exactly at `/home/user/audit_trail.enc`.
- The `/home/user/sandbox` executable must successfully run the daemon when standard input is provided, but immediately terminate it (or cause it to fail gracefully) if the daemon attempts to open a network socket.