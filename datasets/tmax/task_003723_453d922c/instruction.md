You are a security engineer responsible for rotating a compromised application credential and auditing its past usage. The old password, `hunter2`, was accidentally leaked, and you need to deploy a new secret securely. 

Your tasks are:

1. **Log Parsing & Auditing**: 
   Analyze the authentication log located at `/home/user/workspace/auth.log`. Find all unique IPv4 addresses that attempted to authenticate using the compromised password `password=hunter2`. 
   Save these unique IP addresses, one per line, sorted alphabetically, to `/home/user/workspace/compromised_ips.txt`.

2. **Secure Credential Loader (C Programming)**:
   The new credential is saved in `/home/user/workspace/new_secret.txt`. To ensure no corrupted or tampered key is loaded into the production environment, you must write a secure loader in C at `/home/user/workspace/secure_reader.c`.
   
   The C program must meet the following requirements:
   - Accept exactly one command-line argument: the path to the secret file.
   - Read the file and compute its SHA-256 hash using the OpenSSL crypto library (`<openssl/sha.h>`).
   - Compare the computed hash to the known-good hex string: `2abf9b2d87a2a07cb63a4365b210202fc0e6760ba2502ef893fcff5afcc42fc8`.
   - If the hash does *not* match, print an error to `stderr` and exit with status 1.
   - If the hash matches, the process must sandbox itself before outputting the secret. Enable strict seccomp mode using `prctl(PR_SET_SECCOMP, SECCOMP_MODE_STRICT)`. (Remember that strict seccomp only permits `read`, `write`, `_exit`, and `sigreturn` syscalls. You must ensure the file contents are already in memory and you only write to standard output after this point).
   - Write the exact contents of the secret file to `stdout` and exit cleanly.

3. **Execution**:
   Compile your program:
   `gcc /home/user/workspace/secure_reader.c -o /home/user/workspace/secure_reader -lcrypto`
   
   Run your program and save the verified secret:
   `/home/user/workspace/secure_reader /home/user/workspace/new_secret.txt > /home/user/workspace/verified_secret.txt`

Ensure all output files are placed exactly as requested.