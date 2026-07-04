You are a system administrator tasked with automating a local deployment pipeline and setting up a secure static file server. 

Complete the following objectives in the `/home/user` directory:

1. **TLS Web Server:**
   - Generate a self-signed RSA 2048-bit certificate and private key without a passphrase. Store them as `/home/user/certs/cert.pem` and `/home/user/certs/key.pem`.
   - Write a Python script `/home/user/server.py` that serves the directory `/home/user/webroot/latest` over HTTPS on port 8443 using the generated certificate and key. 
   - Start this server in the background and save its PID to `/home/user/server.pid`.

2. **Automated Interactive Deployment (Expect/Filesystem):**
   - There is a mock interactive deployment tool at `/home/user/bin/approve_release.sh` (already existing). It takes a filename as an argument, prompts "Approve deployment of <filename>? (yes/no): ", and requires the exact string "yes" to exit successfully (exit code 0).
   - Write a Python script `/home/user/deploy.py` that uses the `pexpect` module (or calls an `expect` script) to automate the approval of `/home/user/staging/app-v1.0.tar.gz`.
   - Once approved (exit code 0), your script must extract the contents of `/home/user/staging/app-v1.0.tar.gz` into a new directory: `/home/user/deployments/app-v1.0/`.
   - Update the symlink at `/home/user/webroot/latest` to point to `/home/user/deployments/app-v1.0/`.
   - Write a log entry to `/home/user/deploy.log` in the exact format: `SUCCESS: app-v1.0 deployed`

3. **Execution:**
   - Execute your deployment script so that the staging file is processed, the symlink is updated, and the HTTPS server is actively serving the extracted content.

Constraints:
- All required parent directories (`certs`, `webroot`, `deployments`) must be created by you if they don't exist.
- Do not use root/sudo. Use only Python 3 standard libraries and `pexpect`.