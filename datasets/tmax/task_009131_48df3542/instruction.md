You are a DevSecOps engineer tasked with enforcing security policies as code and demonstrating a vulnerability in an internal Go-based microservice before patching it. 

The microservice code is located at `/home/user/server.go`. It has an authentication flaw and a logging flaw.

Your objectives are:

1. **Authentication Flow Testing & Exploit Crafting**:
   The microservice runs on port 8080 and has an endpoint `/secure/key` that returns a highly sensitive SSH private key. It is protected by JWT authentication, but the validation logic is flawed. 
   Write a Go program at `/home/user/exploit.go` that:
   - Crafts a forged JWT with the algorithm (`alg`) set to `"none"` and a payload containing `{"role": "admin"}`.
   - Sends a `GET` request to `http://localhost:8080/secure/key` using the forged JWT in the `Authorization: Bearer <token>` header.
   - Saves the raw, exact response body (the SSH private key) to `/home/user/stolen_key.pem`.
   *(You may need to run `go run /home/user/server.go &` in the background to test your exploit).*

2. **Security Log Parsing & Sensitive Data Redaction**:
   The microservice has been leaking sensitive authentication data into its logs. An existing log file is located at `/home/user/audit.log`.
   Write a Go program at `/home/user/redact.go` that reads `/home/user/audit.log` and produces a sanitized version at `/home/user/audit_clean.log`.
   Your redaction logic must:
   - Find any JWT token (a string following `Bearer ` up to the next space or newline) and replace the token itself with the exact string `[REDACTED]`.
   - Find any plain-text password in URL parameters or form bodies (a string following `password=` up to the next space, `&`, or newline) and replace the password value with `[REDACTED]`.

3. **SSH Hardening**:
   The compromised SSH key was meant for a legacy system. To prevent future lateral movement, you must define an SSH hardening policy. Create a configuration file at `/home/user/sshd_config.policy` containing exactly these three configuration lines (one per line, in any order) to secure the SSH daemon:
   - Disable root login
   - Disable password authentication
   - Disable X11 forwarding

Ensure all created files have the exact names and paths specified above. Do not modify the original `/home/user/audit.log`.