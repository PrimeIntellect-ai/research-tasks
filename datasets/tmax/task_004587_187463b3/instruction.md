You are a forensics analyst recovering evidence from a compromised Linux host. The incident response team has collected several artifacts from the compromised machine and placed them in `/home/user/evidence/`. Your job is to analyze these files, extract threat intelligence, identify the root cause of the breach, and provide remediation configurations.

You must complete the following four phases using Bash commands and scripts:

**Phase 1: Payload Decoding**
The attacker left behind an HTML file (`/home/user/evidence/index.html`). The response team believes the attacker hid the IP address of their Command and Control (C2) server inside an HTML comment starting with `<!-- PAYLOAD: `. 
The payload is doubly encoded: first as a hexadecimal string, which was then Base64 encoded.
Extract this payload, decode it completely, and write ONLY the extracted C2 IP address to `/home/user/c2_ip.txt`.

**Phase 2: Code Auditing**
The initial breach is suspected to have occurred via a vulnerable cron job script located at `/home/user/evidence/backup.sh`. 
Review the script and identify the specific Common Weakness Enumeration (CWE) identifier that represents the vulnerability allowing arbitrary code execution due to improper neutralization of special elements used in an OS command.
Write the exact CWE ID (in the format `CWE-XXX`) to `/home/user/vulnerability.txt`.

**Phase 3: SSH Hardening**
The attacker modified the SSH configuration to maintain persistence. The compromised configuration is located at `/home/user/evidence/sshd_config_compromised`.
Create a hardened version of this file at `/home/user/hardened_sshd_config`. You must modify exactly three directives to secure it:
- Set `PermitRootLogin` to `no`
- Set `PasswordAuthentication` to `no`
- Set `PermitEmptyPasswords` to `no`
Leave all other lines, comments, and spacing exactly as they are in the original file.

**Phase 4: Content Security Policy (CSP)**
To prevent future Cross-Site Scripting (XSS) attacks on the server's web dashboard, we need to enforce a strict Content Security Policy.
Write a single line to `/home/user/csp_meta.txt` containing exactly the HTML `<meta>` tag required to set a Content Security Policy that restricts all content sources (`default-src`) to the same origin (`'self'`). The tag should use the `http-equiv` attribute.

Ensure all output files are placed exactly at the specified paths in `/home/user/`.