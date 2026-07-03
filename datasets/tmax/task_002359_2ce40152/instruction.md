As a security auditor, you have been tasked with building a secure utility to read sensitive log files from a restricted directory. To minimize the risk of vulnerabilities (like arbitrary file reads or code execution) being exploited if your utility is compromised, you must implement strong defense-in-depth measures in C.

Write a C program at `/home/user/secure_reader.c` and compile it to the executable `/home/user/secure_reader`. 

Your program must strictly adhere to the following sequence of operations:

1. **Authentication Token Validation**: 
   Read the `AUTH_TOKEN` environment variable. It must exactly match the string `"AUDITOR_TOKEN_99"`. If it is missing or incorrect, terminate immediately with exit code `1`.

2. **Content Security Policy (Path Enforcement)**:
   The program takes exactly one command-line argument: the absolute path of the file to read.
   Enforce a strict policy to prevent directory traversal:
   - The path must begin exactly with the prefix `/home/user/data/`.
   - The path must NOT contain the substring `..` anywhere.
   If the policy is violated, terminate immediately with exit code `2`.

3. **File Preparation**:
   Open the target file for reading. If the file cannot be opened, terminate with exit code `3`.

4. **Process Isolation (Sandboxing)**:
   Once the file is successfully opened, you must permanently drop the ability to use most system calls by enabling strict seccomp mode. Use `prctl(PR_SET_SECCOMP, SECCOMP_MODE_STRICT, 0, 0, 0)`.
   *(Hint: In strict seccomp mode, only `read()`, `write()`, `_exit()`, and `sigreturn()` are allowed. Standard library functions like `printf()` or `fread()` may implicitly call blocked syscalls like `fstat` or `brk` and cause your process to be killed with SIGSYS).*

5. **Encryption (Obfuscation)**:
   Read the contents of the opened file. Before writing the data, encrypt it by applying a bitwise XOR operation against every byte using the key `0x5A`. 

6. **Output**:
   Write the XOR-encrypted data directly to standard output (`STDOUT_FILENO`). You may process the file in chunks or character by character.

7. **Clean Exit**:
   Once reading and writing are complete, terminate gracefully with exit code `0`.

**Setup Information:**
Before you test your program, create the directory `/home/user/data/` and place a test file there to ensure your code works. Ensure your final binary is compiled to `/home/user/secure_reader`. You are free to use standard GNU/Linux tools to test your work.