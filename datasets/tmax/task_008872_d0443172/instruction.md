You are a security auditor tasked with reviewing a simulated environment for a client. Your objective is to identify vulnerabilities, crack credentials, audit code, and secure configurations. All your work must be done using bash and standard Linux command-line utilities.

The client's environment is located in `/home/user/app/`. They have a legacy Bash-based CGI script used for authentication. 

You must complete the following phases:

**Phase 1: Password Cracking**
The file `/home/user/app/passwd.db` contains a list of usernames and unsalted MD5 hashed passwords. A dictionary file is provided at `/home/user/wordlist.txt`.
1. Write a bash script or one-liner to crack the password for the user `admin`.
2. Save the cracked plaintext password to `/home/user/cracked_password.txt`.

**Phase 2: Open Redirect Exploitation (CWE-601)**
The script `/home/user/app/login.cgi` simulates a CGI authentication flow, using the `QUERY_STRING` environment variable to read inputs (`user`, `pass`, and `redirect`).
1. Invoke the script locally by setting the `QUERY_STRING` environment variable so that it logs in as `admin` (using the cracked password) and attempts to redirect the user to `http://evil.com`.
2. Save the exact raw output (including headers and body) of this successful exploit invocation to `/home/user/vuln_headers.txt`.

**Phase 3: Secure Coding & Patching**
Audit and patch the `/home/user/app/login.cgi` file to fix the Open Redirect vulnerability.
1. Modify `/home/user/app/login.cgi` so that if the extracted `REDIRECT` variable starts with `http://`, `https://`, or `//`, it is overridden and set to `/dashboard`.
2. Keep the rest of the script's logic intact.

**Phase 4: Permissions Review**
The client stored their database insecurely.
1. Change the permissions of `/home/user/app/passwd.db` so that only the owner has read and write permissions (no execute), and no one else has any permissions.

**Phase 5: SSH Hardening**
The client has provided their SSH configuration file at `/home/user/ssh_config`. 
1. Edit `/home/user/ssh_config` to enforce the following security rules:
   - Disable root login (`PermitRootLogin no`)
   - Disable password authentication (`PasswordAuthentication no`)
   - Ensure these uncommented, exact directives exist in the file. Overwrite or modify existing insecure directives.

Ensure all outputs strictly follow the requested file paths.