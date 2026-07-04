You are a security auditor tasked with fixing an open redirect vulnerability in a compiled web server binary, but you must first recover the administrative SSH credentials to access it.

Here is your workflow:
1. **Credential Recovery**: We have intercepted a screen recording of an automated key rotation process, saved at `/app/key_video.mp4`. The video flashes a sequence of QR codes. Extract the frames, decode the QR codes in chronological order, and concatenate the decoded text. This will give you the passphrase for the encrypted SSH private key located at `/app/admin_key`.
2. **Access & Retrieval**: Use the recovered passphrase to unlock `/app/admin_key`. Use this key to SSH into the local test server (`ssh -p 2222 admin@localhost`). Download the target ELF binary located at `/opt/vulnerable_server` on the remote host to your local directory at `/home/user/vulnerable_server`.
3. **Binary Analysis & Redaction**: The binary is a compiled Go web server that contains an open redirect vulnerability tied to a hardcoded internal backend. Write a Go program at `/home/user/patcher.go` that:
   - Reads the ELF binary `/home/user/vulnerable_server`.
   - Locates all occurrences of the sensitive URL string `http://super-secret-backend.local/` (35 bytes) in the binary's data sections.
   - Overwrites these occurrences exactly with the redacted string `http://redacted-secure-domain.com/` (also 35 bytes).
   - Saves the modified executable to `/home/user/patched_server` and ensures it is executable.
   - Computes the SHA256 checksum of the patched binary and writes the hex string to `/home/user/checksum.txt`.
4. **Testing**: Run your Go program to produce the patched binary. 

An automated verification script will spin up your `/home/user/patched_server` on port 8080 and test 10 different open redirect payloads. Your goal is to achieve a 100% success rate (metric threshold: 1.0) where the server redirects to the safe redacted domain without breaking the ELF structure or HTTP functionality.