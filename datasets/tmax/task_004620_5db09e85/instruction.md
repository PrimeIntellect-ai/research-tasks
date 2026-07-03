You have been tasked with securing a multi-service web application stack located in `/app/vulnerable_stack`. The stack consists of an Nginx reverse proxy, a Bash-based CGI login service, and a mock internal service. 

Currently, the stack suffers from an open redirect vulnerability, misconfigured file permissions on executable binaries, and an incomplete Nginx configuration. Furthermore, we need a way to detect past exploit attempts in our logs.

Your objectives are to audit the stack, fix the vulnerabilities, write an intrusion detection script, and bring the services online.

**Step 1: Fix Permissions (Service Auditing & Binary Analysis)**
Directory `/app/vulnerable_stack/bin/` contains several mock ELF binaries. Some of these files have been deployed with insecure permissions (e.g., SUID bits set incorrectly or world-writable).
- Identify all files in `/app/vulnerable_stack/bin/` that have the SUID bit set OR are world-writable.
- Remove the SUID bit and world-writable permissions from these files. Ensure they remain executable by the owner.

**Step 2: Patch the Open Redirect (Secure Coding in Bash)**
The login service is a Bash CGI script located at `/app/vulnerable_stack/cgi-bin/login.cgi`. It parses the `next` query parameter and redirects the user.
- Currently, it blindly redirects to any URL provided in the `next` parameter (e.g., `http://evil.com`).
- Modify `/app/vulnerable_stack/cgi-bin/login.cgi` using Bash to validate the `next` parameter. 
- If `next` starts with `http://` or `https://`, or contains a domain name (e.g., `//evil.com`), default the redirect to `/`. 
- Valid internal relative paths (e.g., `/dashboard` or `/settings`) should still redirect properly.

**Step 3: Intrusion Detection Script (Pattern Matching)**
Write a Bash script at `/home/user/detect.sh` that takes an Nginx access log file path as its first argument.
- The script must scan the log for HTTP GET requests to the `/login` endpoint where the `next` parameter attempts an external redirect (contains `http://`, `https://`, or `//`).
- The script should extract the IP addresses of the attackers making these requests.
- Output ONLY the unique IP addresses, one per line.

**Step 4: Fix Nginx Config and Start the Stack**
The file `/app/vulnerable_stack/nginx.conf` is missing the routing for the CGI login service.
- Edit `/app/vulnerable_stack/nginx.conf` so that requests to `/login` are proxied via `fastcgi_pass` to `127.0.0.1:8081` (the Bash CGI service).
- Ensure the Nginx reverse proxy listens on port `8080`.
- Once configured, start the stack by executing `/app/vulnerable_stack/start.sh`. Leave the services running in the background.

Verify your work by ensuring Nginx is listening on 8080, and testing the open redirect patch using `curl`.