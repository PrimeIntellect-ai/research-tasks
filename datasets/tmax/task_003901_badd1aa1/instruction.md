You are acting as a penetration tester and DevSecOps engineer. You have been granted access to a local staging environment that hosts a web application and an administrative SSH service. Your objective is to automate the vulnerability scanning of these services using Bash, and then patch the discovered vulnerabilities by reconfiguring the services and fixing file permissions.

The environment consists of multiple services managed by a script. They are located in `/home/user/app/`.
- **Backend App:** A Python Flask app listening on `127.0.0.1:5000`.
- **Reverse Proxy:** An Nginx instance listening on `127.0.0.1:8080`, proxying traffic to the Flask app. Its configuration is at `/home/user/app/nginx/nginx.conf`.
- **Admin SSH:** A local, unprivileged OpenSSH daemon listening on `127.0.0.1:2222`. Its configuration is at `/home/user/app/ssh/sshd_config`.

**Step 1: Automated Vulnerability Scanning (Bash)**
Write a Bash script at `/home/user/scan.sh` that acts as a simple automated vulnerability scanner. The script should:
1. Make an HTTP GET request to `http://127.0.0.1:8080/`.
2. Inspect the HTTP response headers.
3. Check for the presence of the `X-Frame-Options` and `X-Content-Type-Options` headers.
4. Check the `Set-Cookie` header to ensure it contains both the `Secure` and `HttpOnly` flags.
5. Inspect the local SSH host key at `/home/user/app/ssh/ssh_host_ed25519_key` to check if its file permissions are overly permissive (i.e., readable by anyone other than the owner).
6. Output its findings. Run this script and save its output to `/home/user/pre_report.txt`.

**Step 2: Hardening and Remediation**
Based on typical security standards, fix the environment:
1. **HTTP Headers & Cookies:** Modify `/home/user/app/nginx/nginx.conf` so that Nginx injects the `X-Frame-Options: DENY` and `X-Content-Type-Options: nosniff` headers. Additionally, modify the Nginx configuration to rewrite or ensure the `Set-Cookie` header from the upstream Flask app always includes `Secure; HttpOnly` (or configure the proxy to append these flags).
2. **SSH Hardening:** Modify `/home/user/app/ssh/sshd_config` to:
   - Disable password authentication completely (`PasswordAuthentication no`).
   - Disable empty passwords.
   - Restrict allowed ciphers to only `chacha20-poly1305@openssh.com` and `aes256-gcm@openssh.com` (use the `Ciphers` directive).
3. **File Permissions:** Fix the permissions of the SSH host key `/home/user/app/ssh/ssh_host_ed25519_key` so it is only readable by the owner (0600).

**Step 3: Apply and Verify**
Restart the services to apply your configurations using the provided script:
`/home/user/app/restart.sh`

Run your scanner script again and save the post-remediation output to `/home/user/post_report.txt`. Ensure the services remain running, as an automated verifier will connect to ports 8080 and 2222 to validate the protocols.