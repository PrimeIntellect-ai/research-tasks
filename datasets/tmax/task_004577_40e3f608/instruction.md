You are a FinOps analyst tasked with preventing developers from provisioning excessively expensive cloud infrastructure, specifically preventing the deployment of expensive GPU instances via Terraform. You need to implement a localized Git-based cost control system.

Your environment is a standard Linux system. You have standard user privileges (no root/sudo). Your home directory is `/home/user`.

Perform the following tasks:

1. **Git Server & Hook:**
   - Create a bare Git repository at `/home/user/finops_repo.git`.
   - Write a `pre-receive` hook (in Bash) for this bare repository.
   - The hook must intercept pushes and check the diff of all newly pushed commits (`oldrev` to `newrev`).
   - If the push adds a line containing exactly `+instance_type = "p4d.24xlarge"` (ignoring leading whitespace on the line, but matching the text exactly) in any file ending with `.tf`, the hook must:
     a) Output exactly "Cost limit exceeded!" to stderr.
     b) Reject the push (exit with a non-zero status).
     c) Append the following exact string to `/home/user/www/cost_report.html` on a new line: `<li><span class="commit">NEWREV</span> - <span class="status">REJECTED</span></li>` (where NEWREV is the newly pushed commit hash).
   - If the push does *not* contain the restricted instance type, the hook must:
     a) Accept the push (exit 0).
     b) Append the following exact string to `/home/user/www/cost_report.html` on a new line: `<li><span class="commit">NEWREV</span> - <span class="status">ACCEPTED</span></li>`.

2. **Web Server & TLS:**
   - Create a directory `/home/user/www`.
   - Initialize `/home/user/www/cost_report.html` with exactly `<ul>\n` (it will be appended to by the git hook).
   - Generate a self-signed TLS certificate (`cert.pem`) and private key (`key.pem`) without a passphrase in `/home/user/www/`. Use any dummy subject data you like.
   - Write and run a simple Python-based HTTPS web server that serves files from `/home/user/www/` on `127.0.0.1:8443`.
   - Run this web server in the background and save its PID to `/home/user/https.pid`.

3. **Port Forwarding:**
   - You need to securely forward traffic from a mock "external" port to your HTTPS server.
   - Use `socat` to listen on TCP port `8080` (bind to `127.0.0.1`) and forward all traffic to your HTTPS server on `127.0.0.1:8443`.
   - Run this `socat` process in the background and save its PID to `/home/user/socat.pid`.

At the end of your task, the bare repository, the running Python HTTPS server, and the running `socat` forwarder must be fully operational. Automated tests will clone your repository, push valid and invalid `.tf` files, verify the hook's rejection/acceptance, verify the HTML log file, and make a `curl` request through port 8080.