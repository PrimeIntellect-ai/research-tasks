You are a network security engineer investigating suspicious activity on a server. You have discovered a compiled binary `/home/user/suspicious_net_helper` that seems to be used as an unauthorized authentication bypass hook for SSH and network traffic inspection.

Your task consists of the following steps:

1. **Reverse Engineering:**
   Analyze the compiled binary `/home/user/suspicious_net_helper` to extract a hardcoded authentication bypass token. The token is a string that, when passed as the first command-line argument, causes the binary to output the string `root`. 

2. **Privilege Escalation Auditing:**
   Search the `/home/user/` directory recursively for any files that have the SUID (Set Owner User ID) bit set, which could represent a privilege escalation risk.

3. **Reporting:**
   Create a report file at `/home/user/audit_report.txt` with exactly the following format:
   ```
   Token: <the_hardcoded_token_you_found>
   SUID: <absolute_path_to_the_suid_file>
   ```

4. **Secure Coding & Permissions:**
   Write a secure replacement in C. Create a file `/home/user/secure_net_helper.c` that accepts exactly one command-line argument. 
   - If the argument is exactly `admin`, it should print `ACCESS GRANTED` to standard output.
   - For any other argument, or if no arguments are provided, it should print `ACCESS DENIED` to standard output.
   - Compile this file to `/home/user/secure_net_helper`.
   - Lock down the compiled binary by setting its file permissions so that ONLY the owner can read and execute it (no write permissions, and absolutely no permissions for group or others).

Complete all steps ensuring that the final files and permissions strictly match the requirements.