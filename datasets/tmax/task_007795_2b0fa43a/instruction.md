You are a DevSecOps engineer tasked with enforcing policy-as-code, auditing services, and mitigating vulnerabilities in a local development environment. You need to complete four specific objectives.

**Environment Setup**
Assume the following files exist in your home directory (`/home/user/`):
- `scan_data.json`: A JSON file containing output from a recent network and service audit.
- `webapp/app.py`: A simple Python Flask application running locally.
- `ssh_configs/sshd_config`: A baseline SSH configuration file.

**Objective 1: Data Processing & Service Auditing**
Read `/home/user/scan_data.json`. This file contains an array of objects representing scanned services. Write a script in any language to parse this data and identify non-compliant services.
A service is non-compliant if EITHER:
- It has `"encryption": "none"` and is exposed on a port other than 80.
- It has `"cve_count"` greater than 0.
Output the non-compliant services to `/home/user/vulnerable.csv` with exactly the following headers: `IP,Port,Service,Reason`.
For the `Reason` column, use "Unencrypted" if `encryption` is none, or "CVEs Found" if `cve_count > 0`. If both apply, use "Critical". Sort the CSV by Port in ascending order.

**Objective 2: Exploit Crafting**
The `/greet` endpoint in `webapp/app.py` takes a `name` query parameter and reflects it directly into the HTML response, making it vulnerable to Cross-Site Scripting (XSS).
Craft a basic XSS payload that would execute `alert(document.domain)` when a user visits the `/greet` endpoint. Save the exact payload string (just the value of the `name` parameter, not URL-encoded) into `/home/user/xss_payload.txt`. 

**Objective 3: Content Security Policy Enforcement**
Fix the vulnerability in `/home/user/webapp/app.py` by implementing a strict Content Security Policy (CSP). Modify the Flask application code so that EVERY response includes the following HTTP header:
`Content-Security-Policy: default-src 'self'; script-src 'none';`
Do not change the routing logic; just ensure the headers are properly injected into the response.

**Objective 4: SSH Hardening (Policy as Code)**
You must harden the SSH configuration found at `/home/user/ssh_configs/sshd_config`. Write a script to read the file and enforce the following rules:
- Set `PermitRootLogin` to `no`
- Set `PasswordAuthentication` to `no`
- Add or enforce the `Ciphers` line to be exactly: `Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com`
Save the modified configuration to `/home/user/ssh_configs/sshd_config_hardened`. Ensure that existing configurations not conflicting with the above are preserved.

Ensure all output files are placed exactly at the specified absolute paths.