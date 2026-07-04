You are an incident responder investigating a suspected compromised web server. The attackers left behind a suspicious executable payload and a client certificate used for mutual TLS authentication. You need to safely analyze these artifacts.

Artifacts provided:
- `/home/user/dropper` (The suspicious binary payload)
- `/home/user/cert.pem` (The intercepted client certificate)
- `/home/user/ca.crt` (The web server's trusted Certificate Authority)

Perform the following investigative steps:

1. **Certificate Chain Validation:**
   Use the `openssl` command-line tool to verify the intercepted client certificate (`/home/user/cert.pem`) against the trusted CA (`/home/user/ca.crt`). Redirect the standard output and standard error of this verification command to `/home/user/cert_verify.log`.

2. **Secure Automated Analysis (C++):**
   Write a C++ program at `/home/user/analyzer.cpp` that performs automated, isolated execution and hashing of the payload. Your C++ program must:
   - Compute the SHA-256 hash of the `/home/user/dropper` file (you may use OpenSSL's `libcrypto` via `<openssl/sha.h>`).
   - Write the lowercase, hex-encoded SHA-256 hash string to `/home/user/dropper_hash.txt`.
   - Safely execute the `/home/user/dropper` executable inside a sandbox using process isolation to prevent it from modifying the system or communicating externally. You must invoke the `bwrap` (Bubblewrap) command-line utility from within your C++ program with the following exact isolation arguments: 
     `bwrap --ro-bind / / --dev /dev --unshare-all /home/user/dropper`
   - Capture the standard output of this sandboxed execution and write it directly to `/home/user/dropper_output.txt`.

3. **Compilation and Execution:**
   Compile your analyzer:
   `g++ -o /home/user/analyzer /home/user/analyzer.cpp -lcrypto`
   Run the analyzer:
   `/home/user/analyzer`

Ensure all output files (`cert_verify.log`, `dropper_hash.txt`, `dropper_output.txt`) are created successfully and contain the correct data.