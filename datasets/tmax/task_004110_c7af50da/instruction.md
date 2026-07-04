You are acting as a security auditor. You have been assigned to review a data processing module on a Linux system. The working directory for this task is `/home/user/audit`.

Within this directory, you will find:
1. `auth_helper.c`: A small C program that processes a secret password.
2. `server.crt`: An X.509 certificate.
3. `ca.crt`: A Root CA certificate.

Your tasks are as follows:

1. **Code Audit & Remediation (CWE Identification & Fix):** 
   The `auth_helper.c` script currently accepts a sensitive password via command-line arguments (e.g., `./auth_helper my_secret_password`). This is a security vulnerability because command-line arguments are visible system-wide via `/proc` (specifically `/proc/[pid]/cmdline`) and process monitoring tools like `ps`.
   - Identify the most specific CWE identifier for this vulnerability (passing sensitive information via command-line arguments).
   - Modify `auth_helper.c` so that it no longer accepts the password via `argv`. Instead, it must read the password from an environment variable named `AUTH_PASS`. If `AUTH_PASS` is not set or is empty, the program should exit with status code `1`. The program must output exactly the same success message format as before: `Processing with secret: <password>`.
   - Compile your fixed code into an executable named `/home/user/audit/auth_helper_fixed` using `gcc`.

2. **Certificate Validation:**
   - Verify if `server.crt` is validly signed by the Certificate Authority `ca.crt`. 

3. **Checksum Generation:**
   - Compute the SHA-256 hash of your modified `auth_helper.c` file.

4. **Reporting:**
   Create a log file at `/home/user/audit/report.txt` with exactly three lines containing your findings:
   - **Line 1:** The exact CWE identifier for the command-line argument leakage vulnerability (e.g., `CWE-XXX`). Use the standard CWE prefix. (Hint: Look for "Invocation of Process Using Visible Sensitive Information").
   - **Line 2:** The result of the certificate validation. Write exactly `VALID` if the chain is valid, or `INVALID` if it is not.
   - **Line 3:** The exact SHA-256 hash (hexadecimal) of your modified `auth_helper.c` file.