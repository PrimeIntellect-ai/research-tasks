You are a compliance analyst tasked with generating an audit trail for a legacy system and hardening our internal access points. You must complete the following multi-stage setup:

1. **SSH Hardening & Key Management:**
   Configure and run a local instance of the OpenSSH server (`sshd`) that runs as the current user (`user`).
   - It must listen on `127.0.0.1` port `2222`.
   - Disable password authentication; only public key authentication must be allowed.
   - Restrict cryptographic algorithms to exactly the following:
     - Key Exchange (KexAlgorithms): `curve25519-sha256@libssh.org`
     - Ciphers: `chacha20-poly1305@openssh.com`
     - MACs: `hmac-sha2-512-etm@openssh.com`
   - Trust the following public key for the `user` account (add it to the appropriate authorized keys file):
     `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMYyHq/MdfiQ/hXmR9T7C8yWwGqK3yB7a1s7Q/X4zW2a audit-key`
   - Generate any necessary host keys and run the `sshd` daemon in the background using your custom configuration.

2. **Automated Vulnerability Scanning:**
   To prove the SSH server is properly hardened, run an automated scan against your SSH server on port 2222 using `nmap`. Output the scan results in XML format to `/home/user/ssh_scan.xml`. Ensure the scan enumerates the SSH algorithms to prove compliance (e.g., using the `ssh2-enum-algos` script).

3. **Payload Decoding and Audit Service:**
   We have a proprietary legacy audit sender located at `/app/legacy_audit_sender` (a stripped binary). This binary sends audit events to a central logging server.
   - It expects a web server to be listening on `127.0.0.1:8080`.
   - It sends HTTP POST requests to the `/ingest` endpoint.
   - The payload in the POST body is encoded. You must analyze the binary (using tools like `strings`, `objdump`, or by running it and capturing traffic) to determine the encoding scheme. (Hint: It uses a combination of a standard encoding and a simple single-byte XOR).
   - Write and run a web service (in Python, Node.js, Ruby, or any language of your choice) on port 8080.
   - Your service must receive the POST request, decode the payload to its original plaintext string, and append the decoded plaintext string (followed by a newline) to `/home/user/audit_trail.log`.

Ensure both the SSH server and the HTTP audit service are running in the background when you complete the task. Do not stop them.