You are a forensics analyst responding to a compromised host. The attacker installed a backdoor into a local, vendored web framework and exfiltrated data. You need to secure the system, patch the backdoor, and bring up hardened services to safely capture the attacker's automated callback attempts.

You have the following artifacts:
1. A vendored copy of the `bottle` web framework located at `/app/bottle-0.12.25/`. The attacker modified this package to include a backdoor triggered by specific HTTP headers and cookies.
2. An evidence log file at `/app/evidence/access.log` which contains the payload the attacker used to drop their SSH public key onto the system via the backdoor.

Your objectives:

**1. Analyze and Fix the Vendored Package (Vulnerability Analysis & Secure Coding)**
Examine `/app/bottle-0.12.25/bottle.py`. The attacker injected a backdoor that parses a malicious HTTP header and Cookie to execute arbitrary code. 
- Identify the perturbation and remove the backdoor code entirely. 
- Ensure the package works as originally intended for standard HTTP requests.

**2. Deploy a Secure Evidence Server (Content Security Policy & Injection protection)**
Create a Python script `/home/user/server.py` that uses the *fixed* `/app/bottle-0.12.25` framework.
- It must listen on `127.0.0.1:8000`.
- It must serve an endpoint `GET /evidence` that returns the plaintext string `Evidence Secure`.
- To prevent XSS, every response from this server must include the exact HTTP header: `Content-Security-Policy: default-src 'self'`

**3. Recover the SSH Key and Deploy a Hardened SSH Honeypot (SSH Hardening & Key Management)**
Analyze `/app/evidence/access.log`. It contains a base64-encoded or URL-encoded payload in one of the backdoored HTTP requests that drops the attacker's `ssh-rsa` public key.
- Extract this exact public key.
- Configure and start an SSH server listening on `127.0.0.1:2222`. You may use OpenSSH (`/usr/sbin/sshd`) configured to run as the unprivileged `user` account, or write a Python script using `paramiko`.
- The SSH server must accept logins for the username `analyst` **ONLY** if authenticated using the attacker's recovered public key. Password authentication must be strictly disabled.
- The SSH server must stay running in the background.

Ensure both the HTTP server and the SSH server are running continuously. Once both are up and properly configured, output "SERVICES READY" to the console. Automated verifiers will connect to `127.0.0.1:8000` and `127.0.0.1:2222` to exercise the protocols, check the CSP headers, attempt to trigger the backdoor, and test the SSH authentication constraints.