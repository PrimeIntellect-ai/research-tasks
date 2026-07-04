You are acting as a compliance analyst. We have a C++ utility used to decrypt and parse system audit logs. However, during a recent security review, a critical vulnerability was flagged in the log parsing function. Furthermore, to comply with strict sandboxing policies, we must ensure this utility is executed in an isolated environment.

Your objectives:
1. **Code Audit and Fix**: Review the C++ source code located at `/home/user/audit_parser.cpp`. Identify and fix the stack-based buffer overflow (CWE-120/CWE-121) vulnerability in the `parse_record` function. The code currently uses an unsafe string copy mechanism. Fix it so it safely handles strings of any length without overflowing buffers.
2. **Compile**: Compile the fixed C++ code to an executable named `/home/user/audit_parser`. You may need to link against `libcrypto` (OpenSSL) as the utility decrypts AES-256-CBC encrypted logs.
3. **Sandboxed Execution**: We have an encrypted log file at `/home/user/encrypted_logs.dat`. The AES-256-CBC decryption key (hex-encoded) is stored in `/home/user/key.txt`. The IV is prepended to the first 16 bytes of the encrypted file (the C++ code already handles this).
   Write a bash script `/home/user/run_audit.sh` that executes the `/home/user/audit_parser` inside a `bwrap` (Bubblewrap) sandbox. 
   The sandbox must have the following properties:
   - Read-only access to the entire root filesystem (`/`).
   - Read-write access to the `/home/user/audit_output` directory (you must create this directory).
   - Unshare all namespaces (`--unshare-all`).
   - Run the command: `/home/user/audit_parser /home/user/encrypted_logs.dat /home/user/audit_output/decrypted_trail.txt <KEY_FROM_FILE>`
4. Execute your script so that `/home/user/audit_output/decrypted_trail.txt` is successfully generated.

Ensure `/home/user/run_audit.sh` is executable.

Output Format for the parsed log:
The C++ program, once functioning, will output decrypted and parsed lines into the output file. Do not change the existing output formatting logic in the C++ program; only fix the vulnerability.