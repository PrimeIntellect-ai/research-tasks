You are a DevSecOps engineer responsible for enforcing policy as code. We have a C-based microservice called `policy-daemon` located at `/app/policy-daemon`. It uses a vendored lightweight networking library located at `/app/vendored/mongoose`.

During a recent supply chain audit, an automated vulnerability scanner flagged an issue: the build system for the vendored package was modified, and the C server code contains a privilege-handling flaw.

Your objectives:
1. **Cryptographic Checksum Verification**: 
   We have provided a known-good checksum file at `/app/checksums.txt`. Run a checksum verification on the files in `/app/vendored/mongoose` to identify which file was tampered with. Fix the tampered file (it should enable OpenSSL support for the build).
   
2. **TLS Certificate Management**:
   Generate a self-signed 2048-bit RSA TLS certificate (`server.crt`) and key (`server.key`) valid for 365 days. Place them in `/app/policy-daemon/certs/` (create the directory if it doesn't exist).

3. **Secure Coding & Privilege Escalation Auditing**:
   Review `/app/policy-daemon/server.c`. There is a function `drop_privileges_and_init()` that attempts to enforce security policies. However, it fails to securely check the return value of a critical permission check (simulated via an environment variable `MOCK_EUID`). Fix the C code so that if the mock privilege drop fails, the program immediately exits with status code 1.

4. **Integration & Execution**:
   Recompile the `policy-daemon` using the provided `Makefile` in `/app/policy-daemon/`.
   Start the server in the background. It must listen on:
   - `https://localhost:8443/api/policy` (TLS enabled, using your generated certs).
   
   The server expects requests containing the header `Authorization: Bearer devsecops-token-99`. 
   
Leave the server running in the background when you are finished. Create a log file at `/home/user/task_complete.log` containing the word "DONE" once the server is successfully running.