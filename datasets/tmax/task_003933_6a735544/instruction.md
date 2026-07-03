You are a security engineer tasked with rotating credentials and deploying a secure gateway service.

You have received an image backup of a legacy credential at `/app/secret_note.png`. 
Please complete the following workflow:

1. **Extract and Hash the Legacy Secret**:
   - Extract the text from `/app/secret_note.png`.
   - Compute the SHA-256 hash of the extracted text (ensure no trailing newlines are included in the hash).
   - Save the resulting hex hash to `/home/user/old_hash.txt`.

2. **SSH Service Hardening and Rotation**:
   - Generate a new Ed25519 SSH keypair at `/home/user/admin_key` with no passphrase.
   - Generate an Ed25519 host key for the SSH server at `/home/user/host_key` with no passphrase.
   - Create an SSH configuration file at `/home/user/sshd_config` that runs on port `2222`.
   - The SSH server must use `/home/user/host_key` as its host key.
   - Configure it to use `/home/user/.ssh/authorized_keys` for authorization, and add your newly generated `admin_key.pub` to it.
   - Disable password authentication and disable StrictModes.
   - Set the PidFile to `/home/user/sshd.pid`.
   - Start the SSH daemon as the current user using this configuration.

3. **Secure Web Gateway (Bash)**:
   - Create a Bash script at `/home/user/httpd.sh` that acts as a simple HTTP server listening on port `8080`.
   - It must respond to HTTP GET requests with a valid `HTTP/1.1 200 OK` response.
   - The HTTP response must enforce a Content Security Policy by including the header: `Content-Security-Policy: default-src 'none';`
   - The body of the response must be `Secure System`.
   - Run this script in the background so the port remains open and responsive.

Ensure both the SSH service (port 2222) and the web gateway (port 8080) are actively running and bound to 127.0.0.1 or 0.0.0.0 before completing your task.