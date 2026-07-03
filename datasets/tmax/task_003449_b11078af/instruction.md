You are acting as a security auditor reviewing a legacy HTTP data processing system. 

You have been provided with a directory `/home/user/audit/` containing the following items:
1. `target_binary`: A compiled C++ executable used to process logs. It contains a hardcoded, highly privileged HTTP cookie token used for legacy admin authentication.
2. `http_logs.txt`: A file containing raw HTTP request headers and associated source IP addresses.
3. `sys_files/`: A simulated root directory tree representing the system where the application is deployed.

Your objective is to complete a comprehensive security audit by performing the following steps:

1. **Reverse Engineering:**
   Analyze the compiled `target_binary` (e.g., using `strings`, `objdump`, or other analysis tools) to extract the hardcoded secret admin token. The token is a string that starts with `X-Admin-Token: `. 

2. **HTTP Header and Cookie Inspection (via C++):**
   Write a C++ program named `/home/user/cookie_extractor.cpp`. This program must:
   - Read `/home/user/audit/http_logs.txt`.
   - Parse the HTTP headers to identify which requests contain the exact admin token you extracted from the binary.
   - Extract the source IP address of any request containing the admin token.
   - Output these IP addresses, one per line, to a file named `/home/user/admin_ips.txt`.
   Compile and execute your C++ program.

3. **Privilege Escalation Auditing:**
   The application is suspected of executing external scripts with elevated privileges. Audit the `/home/user/audit/sys_files/` directory tree to find any file that is world-writable (which would allow a local attacker to escalate privileges). 
   Once you identify the world-writable file, write its absolute path to `/home/user/vuln_file.txt`.

Ensure your C++ code is robust and your output files exactly match the required formats.