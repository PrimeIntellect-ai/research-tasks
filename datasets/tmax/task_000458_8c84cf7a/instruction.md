As a DevSecOps engineer, you are tasked with analyzing a security incident and deploying a hardened policy-as-code environment to prevent future occurrences. An incident recording has been provided to you at `/app/incident_record.mp4`. This video contains a terminal screen capture showing the attacker's SSH public key and a hex dump of an ELF binary containing a hardcoded malicious redirect payload.

Your objective is to complete the following multi-phase task using Bash as your primary implementation language:

1. **Forensic Extraction**:
   - Extract the base64-encoded SSH `ed25519` public key visible in the terminal output within the video.
   - Extract the malicious fully qualified URL (the exploit payload) exposed in the ELF binary hex dump shown later in the video.

2. **SSH Hardening & Key Management**:
   - Configure and run an SSH server (running as a non-root user) listening strictly on `127.0.0.1:2222`.
   - The SSH server must only allow public key authentication for the user `user`.
   - Authorize ONLY the exact SSH public key extracted from the video.
   - Harden the SSH configuration to disable password authentication, disable root login (even if root were possible), and restrict the `KexAlgorithms` to `curve25519-sha256@libssh.org`.

3. **Secure Redirect Gateway (Open Redirect Mitigation)**:
   - Create a Bash script named `/home/user/gateway.sh` that acts as a web server using `socat` or `nc`, listening on `127.0.0.1:8080`.
   - The service must handle HTTP GET requests to `/redirect?target=<URL>`.
   - Implement policy-as-code to mitigate the open redirect: 
     - If the `<URL>` exactly matches the malicious URL extracted from the ELF binary in the video, the server must respond with a strict `403 Forbidden` HTTP status.
     - If the `<URL>` is a relative path (e.g., `/dashboard`), it must respond with a `302 Found` redirecting to that path.
     - Any other external URL should also receive a `403 Forbidden`.

Ensure both the SSH service on port 2222 and the HTTP gateway on port 8080 are running in the background before completing your task. Create a log file at `/home/user/deployment.log` containing the extracted malicious URL on the first line, and the extracted SSH public key on the second line.