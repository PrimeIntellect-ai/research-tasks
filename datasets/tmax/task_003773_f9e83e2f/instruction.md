You are a Linux Systems Engineer responsible for setting up and hardening a local web service.

You have been provided with the source code of a third-party bash-based web server, `bashttpd`, located at `/app/bashttpd`. 

Your objectives are:

1. **Fix the Web Server:**
   The `bashttpd` script at `/app/bashttpd/bashttpd` has a deliberate perturbation (a bug) introduced recently that causes it to fail to send the correct HTTP response headers. Identify and fix the typo in the script.

2. **Backup the Configuration:**
   A preliminary configuration directory exists at `/home/user/config_template/`. Before proceeding, create a backup of this directory. Create a compressed tar archive at `/home/user/config_backup.tar.gz` containing the exact contents of `/home/user/config_template/`.

3. **Configure the Web Server:**
   Copy the `bashttpd.conf` file from `/home/user/config_template/` to `/home/user/`. Edit `/home/user/bashttpd.conf` to configure the server to serve files from the `/home/user/www/` directory.

4. **TLS Configuration & Expect Scripting:**
   The service must be served securely over HTTPS.
   - Generate a self-signed RSA TLS certificate (`/home/user/cert.pem`) and a password-protected private key (`/home/user/key.pem`). Use the exact password `HardenedPass123` for the private key.
   - You need to run a TLS termination proxy that listens on `127.0.0.1:8443` and forwards traffic to your `bashttpd` server listening on `127.0.0.1:8080`.
   - Write an Expect script at `/home/user/start_service.exp` that automates starting the TLS proxy (using `openssl s_server`, `socat`, or `stunnel` depending on your preference) and automatically provides the private key password `HardenedPass123` to the interactive prompt. 
   - The expect script must also ensure `bashttpd` is running on `127.0.0.1:8080`. 
   - Execute your expect script so the HTTPS server is running in the background and listening on `127.0.0.1:8443` when you finish.

Verify your setup by ensuring a client can connect via HTTPS to `127.0.0.1:8443` and retrieve the contents of `/home/user/www/index.html`. 
Leave the service running on port 8443.