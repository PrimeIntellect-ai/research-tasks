You are a forensics analyst investigating a compromised host. The attacker exploited an Open Redirect vulnerability in the login flow of a custom lightweight web server written in C, hijacked an admin session, and left behind an encrypted evidence file containing a rogue certificate chain.

Your objective is to patch the web server, crack the evidence archive, validate the rogue certificates, and secure the recovered files.

Complete the following steps:

1. **Vulnerability Analysis & Secure Coding (C):**
   Examine the source code of the web server located at `/home/user/server.c`. Find the HTTP GET parameter used for redirection after login that is vulnerable to an Open Redirect (it blindly accepts full URLs).
   Patch the C code to prevent the Open Redirect. The patched code should ensure that the redirect URL strictly starts with a single forward slash `/` and does not contain `http://` or `https://` before redirecting. If it is an invalid redirect, default the redirect to `/home`. 
   Compile the patched file using: `gcc /home/user/server.c -o /home/user/server_patched`

2. **Password Cracking:**
   The attacker left an encrypted zip file at `/home/user/evidence.zip`. Intelligence suggests the password is the name of the vulnerable parameter you identified in Step 1, concatenated with a 4-digit PIN (e.g., if the parameter was `next_url`, the password would be between `next_url0000` and `next_url9999`).
   Brute-force the password and extract the contents into `/home/user/evidence/`.

3. **Certificate Chain Validation:**
   Inside the extracted `/home/user/evidence/` directory, you will find three certificates: `root.pem`, `intermediate.pem`, and `rogue.pem`.
   Using OpenSSL, verify the certificate chain (`root.pem` -> `intermediate.pem` -> `rogue.pem`). Then, extract the Subject Common Name (CN) of `rogue.pem`.

4. **File Permissions:**
   Forensic best practices dictate that the extracted evidence must be immutable. Change the permissions of all files inside `/home/user/evidence/` so they are strictly read-only for the owner, and have absolutely no permissions for the group or others.

5. **Reporting:**
   Create a final report at `/home/user/report.txt` with exactly three lines in the following format:
   Line 1: The name of the vulnerable parameter.
   Line 2: The 4-digit PIN used in the archive password.
   Line 3: The exact Subject Common Name (CN) of the `rogue.pem` certificate.