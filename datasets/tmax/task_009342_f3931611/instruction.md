You are a monitoring specialist tasked with setting up a secure, localized alert dashboard to analyze legacy authentication logs for silent key rejections. You must complete this task entirely in user space without root access.

Your objectives are as follows:

1. **Mounting the Log Archive:**
   You have been provided with a squashfs archive located at `/home/user/logs.sqsh`.
   Create a directory at `/home/user/mnt_logs` and mount the archive to this directory using `squashfuse` (a user-space FUSE tool). 

2. **Generating Alerts (Bash Scripting):**
   Create a directory called `/home/user/alerts`.
   Write a Bash script at `/home/user/generate_alerts.sh` that searches through all `.log` files in the mounted `/home/user/mnt_logs` directory for any lines containing the exact string `Failed publickey`. 
   The script should output these exact matching lines to a file at `/home/user/alerts/ssh_alerts.txt`.
   Execute your script so the `ssh_alerts.txt` file is generated.

3. **Configuring Permissions (ACL):**
   To ensure the alert file can be read by our external audit tool (which runs under a different user profile), apply an Access Control List (ACL) to `/home/user/alerts/ssh_alerts.txt`. 
   Use `setfacl` to grant read-only (`r`) permissions specifically to the user `nobody` for this file.

4. **Web Server & TLS Setup:**
   Generate a self-signed RSA-2048 TLS certificate and private key. Save them as `/home/user/cert.pem` and `/home/user/key.pem` respectively (use no passphrase, and standard defaults for the subject are fine).
   Write a Bash script at `/home/user/serve.sh` that starts an HTTPS web server on port `8443` serving the `/home/user/alerts` directory. You may use Python's `http.server` combined with the `ssl` module, or `openssl s_server`, or `socat` within your bash script to achieve this. 
   Run your `serve.sh` script in the background so that the alerts are accessible over HTTPS.

Ensure all scripts are executable. The final state of the system should have the archive mounted, the alerts generated and ACLed, the certificates present, and an active TLS listener on port 8443 serving the generated text file.