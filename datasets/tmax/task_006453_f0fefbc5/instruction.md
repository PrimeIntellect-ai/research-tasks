You are acting as a penetration tester verifying a suspected vulnerability in an internal binary. You have intercepted a security log and a set of certificates. 

Your task is to identify the correct exploit payload from the logs, write a C program to safely execute and sandbox the target binary, and record the crash result.

Here are your instructions:

1. **Certificate Validation & Log Parsing**:
   - Check the certificates in `/home/user/certs/`. There is a Root CA (`ca.pem`) and three leaf certificates (`leaf_A.pem`, `leaf_B.pem`, `leaf_C.pem`). Only *one* of these leaf certificates is valid and properly signed by `ca.pem`.
   - Read `/home/user/security.log`. Find the log entry corresponding to the valid leaf certificate.
   - Extract the Base64 encoded payload from that log entry and decode it.

2. **Process Isolation & Sandboxing (C Programming)**:
   - Write a C program at `/home/user/sandbox.c` and compile it to `/home/user/sandbox`.
   - Your C program must accept exactly one command-line argument (the decoded payload).
   - The program must `fork()` a child process.
   - In the child process, apply process isolation using `setrlimit` to restrict file creation: set `RLIMIT_FSIZE` (maximum file size) to a hard and soft limit of `0`.
   - After setting the limit, the child process must execute the binary located at `/home/user/target_bin`, passing the decoded payload as its first argument (i.e., `argv[1]`).
   - The parent process must `wait()` for the child to finish.
   - If the child process is terminated by a signal (indicating a crash/vulnerability), the parent must print exactly: `VULNERABLE: SIGNAL <signal_number>`
   - If the child process exits normally, the parent must print exactly: `SECURE: EXIT <exit_code>`

3. **Execution and Reporting**:
   - Run your compiled `/home/user/sandbox` program using the decoded payload you found in step 1.
   - Redirect the standard output of your `sandbox` program to `/home/user/final_report.txt`.