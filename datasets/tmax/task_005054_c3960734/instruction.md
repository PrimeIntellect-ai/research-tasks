You are a forensics analyst investigating a compromised Linux server. We have captured a snapshot of evidence from the system, located in the directory `/home/user/evidence/`. You need to analyze this evidence to determine how the attacker gained access, maintained persistence, and what actions they took. 

The evidence directory contains the following subdirectories:
- `/home/user/evidence/http/`: Contains web server HTTP request dumps (`requests.log`).
- `/home/user/evidence/ssh/`: Contains the compromised SSH configuration file (`sshd_config`) and `authorized_keys`.
- `/home/user/evidence/bin/`: Contains system binaries and a file `checksums.md5` with known good MD5 hashes.
- `/home/user/evidence/src/`: Contains `auth.js`, the authentication module for the Node.js application running on the server.

Perform the following tasks using standard bash commands:

1. **Authentication Bypass (JWT):** The attacker bypassed authentication by manipulating a JSON Web Token (JWT). Inspect `/home/user/evidence/http/requests.log`. Identify the IP address of the request that successfully passed a JWT with the algorithm set to `none` (hint: the JWT header is base64url encoded).
2. **Vulnerability Analysis:** The attacker initially discovered a SQL injection vulnerability in the application's source code before opting for the JWT bypass. Examine `/home/user/evidence/src/auth.js` and identify the exact line number where the raw user input is concatenated directly into a SQL query.
3. **SSH Hardening Analysis:** To maintain persistence, the attacker modified the SSH daemon configuration. Inspect `/home/user/evidence/ssh/sshd_config`. Identify the exact configuration directive the attacker added or modified to allow insecure root access.
4. **Binary Format & Integrity:** The attacker replaced a system binary with a malicious payload. Validate the files in `/home/user/evidence/bin/` against `checksums.md5`. Once you find the modified (compromised) binary, extract the hidden Command and Control (C2) domain embedded inside it as a string (it starts with `c2.`).

Write your final answers to a file named `/home/user/findings.ini` in the exact format below:

```ini
[Forensics]
Malicious_IP=192.168.x.x
Vulnerable_Line_Number=XX
Insecure_SSH_Config=Directive yes
Compromised_Binary=filename
C2_Domain=c2.example.com
```

Ensure all keys match exactly and contain only the requested data.