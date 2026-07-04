You are a forensics analyst investigating a compromised Linux host. The attacker has wiped most of their tracks but left behind an archived log file, a set of modified server binaries, and a hidden directory.

Your task is to uncover the attacker's tracks, fix the compromised service, and securely expose the evidence for our automated evidence-collection system.

Here are the steps you must complete:

1. **Security Log Parsing**:
   Analyze the authentication log located at `/home/user/auth.log`. The attacker successfully brute-forced or exploited an account named `service_account`. Identify the IP address the attacker used when they *successfully* authenticated as `service_account`.
   Save ONLY this IP address in a file at `/home/user/evidence/attacker_ip.txt`.

2. **File Permission & Access Control**:
   The directory `/home/user/evidence` contains sensitive forensic data. Ensure that ONLY the owner (`user`) has read and write access to the directory and the files within it. Remove all access for group and others (`chmod 700` for the directory, `600` for files).

3. **Vulnerability Remediation & Compilation**:
   The attacker replaced our logging server with a backdoored version of a third-party HTTP server, `darkhttpd-1.14`, located at `/app/darkhttpd-1.14`. 
   - They broke the `Makefile` so it fails to build.
   - They inserted a backdoor in `darkhttpd.c`: any HTTP request containing the header `X-Attacker-Auth: backdoor` bypasses normal directory restrictions.
   Fix the `Makefile` so it compiles successfully using standard `gcc`.
   Audit `darkhttpd.c` to find and completely remove the attacker's backdoor logic.
   Recompile the server.

4. **Service Auditing & Evidence Delivery**:
   Start the compiled `darkhttpd` binary on `127.0.0.1` port `8080`, serving the `/home/user/evidence/` directory.
   The service must run in the background.

Our automated evidence collector will connect to `http://127.0.0.1:8080/attacker_ip.txt` to verify the IP extraction. It will also send malicious requests using the `X-Attacker-Auth: backdoor` header to ensure the vulnerability has been removed and the server does not leak restricted files.