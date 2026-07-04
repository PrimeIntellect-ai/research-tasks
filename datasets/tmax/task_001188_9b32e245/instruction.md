You are a forensics analyst recovering evidence and securing a compromised Linux host. The attackers left behind a stripped binary daemon at `/app/malicious_uploader` which they used as a file stash. 

Your task consists of four main phases:

1. **Binary Analysis & Protocol Reversing**:
   Analyze the stripped binary `/app/malicious_uploader`. Reverse engineer it to determine its custom TCP protocol for uploading files. The daemon listens for incoming connections, receives a filename and file contents, and writes them to disk. Identify the path traversal vulnerability and the specific backdoor filename the attackers used to bypass access controls.

2. **Secure Daemon Implementation (C)**:
   Write a secure replacement daemon in C at `/home/user/secure_uploader.c`. 
   - Compile it to `/home/user/secure_uploader`.
   - It must listen on `127.0.0.1:8080`.
   - It must implement the exact same communication protocol as the malicious binary (so our internal systems can still send evidence files).
   - It must strictly sanitize inputs: reject any filenames containing path traversal characters (`..`, `/`) or the attacker's backdoor filename. Return the string "ERROR: INVALID PATH\n" and close the connection for malicious inputs.
   - For valid inputs, save the uploaded content to `/home/user/evidence_vault/<filename>`.
   - Run this service in the background.

3. **SSH Hardening**:
   Configure a secure local SSH instance for evidence retrieval.
   - Configure SSH to run on port `2222`.
   - Disable password authentication completely; allow only public key authentication.
   - Add the public key provided in `/home/user/investigator.pub` to the authorized keys for the `user` account.
   - Start or restart the SSH service so it is listening on `127.0.0.1:2222`.

4. **Network Isolation**:
   Use `iptables` to secure the host.
   - Set the default INPUT policy to DROP.
   - Allow incoming connections on loopback (`lo`).
   - Allow incoming TCP connections ONLY on port `2222` (for SSH) from any interface.
   - Ensure the secure uploader on port `8080` is only accessible locally.

Log your findings about the original malicious binary's protocol and the exact backdoor filename to `/home/user/forensics_report.txt`. Keep the daemons running for verification.