You are acting as a security auditor for a small application deployment. You have been tasked with securing a custom Rust-based web server, fixing dangerous file permissions, and hardening an SSH configuration template.

Your workspace is located at `/home/user/auditing_workspace`. Within this directory, you will find:
1. `www/` - The web root directory serving static files.
2. `web_server/` - A simple Rust HTTP server project (using standard `std::net`).
3. `sshd_config_custom` - A template SSH configuration file used for the deployment.

Please complete the following security auditing tasks:

**Task 1: File Permission Remediation**
The `www/` directory contains several static assets. Some of these files have been accidentally left with dangerous, overly permissive permissions (e.g., world-writable).
1. Identify all files within `/home/user/auditing_workspace/www/` that are world-writable.
2. Log the absolute paths of these dangerously permissive files to `/home/user/vuln_files.log` (one path per line).
3. Secure the permissions by changing all files in the `www/` directory to standard web-safe permissions (`644` for files, `755` for directories).

**Task 2: Content Security Policy (CSP) Enforcement**
The web server currently does not implement a Content Security Policy, leaving it vulnerable to XSS.
Modify the Rust source code located at `/home/user/auditing_workspace/web_server/src/main.rs`. 
Inject the following exact CSP header into the HTTP response:
`Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted.cdn.com`
Ensure the Rust program compiles successfully after your changes. You do not need to run the server, just ensure `cargo build` succeeds.

**Task 3: SSH Hardening**
The deployment script uses `/home/user/auditing_workspace/sshd_config_custom`. Inspect this file and harden it by making the following explicit changes:
1. Ensure `PermitRootLogin` is set to `no`
2. Ensure `PasswordAuthentication` is set to `no`
Leave the rest of the file intact. If the directives exist, modify them. If they don't, append them.

Do not write your solutions or scripts in the chat. Perform the actions directly in the system.