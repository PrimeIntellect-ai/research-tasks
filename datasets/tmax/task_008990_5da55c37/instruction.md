You are a deployment engineer tasked with rolling out a local continuous deployment (CD) mechanism for a static website. Since you are operating in an unprivileged environment, you cannot use standard system-wide tools like root systemd or the global `/etc/logrotate.d/`.

Your goal is to build an atomic deployment pipeline, a TLS-enabled web server, and a local log rotation setup. 

Here are the exact requirements:

1. **Directories & Repository Setup:**
   - A bare Git repository exists at `/home/user/site_repo.git`. (Assume it contains an `index.html`).
   - Create the following directories:
     - `/home/user/deployments/`
     - `/home/user/certs/`
     - `/home/user/logs/`

2. **TLS Configuration:**
   - Generate a self-signed RSA (2048-bit) certificate and private key in `/home/user/certs/`. Name them `cert.pem` and `key.pem`. 

3. **Web Server:**
   - Write a script in a language of your choice (e.g., Python) at `/home/user/server.py`.
   - The server must listen on `0.0.0.0` (or `127.0.0.1`) port `8443`.
   - It must use TLS (using the generated cert/key).
   - It must serve static files from the directory pointed to by the symlink `/home/user/www-current`.
   - It must append all access logs (or startup messages) to `/home/user/logs/server.log`.

4. **Atomic Deployment Script:**
   - Write a bash script at `/home/user/deploy.sh` that acts as your local CD pipeline.
   - When run, the script must:
     a) Clone the `/home/user/site_repo.git` repository into a new uniquely named directory inside `/home/user/deployments/` (e.g., `/home/user/deployments/release-$(date +%s)`).
     b) Atomically update a symlink at `/home/user/www-current` to point to this new release directory.
     c) Manage the service lifecycle: Find any existing `server.py` process, kill it gracefully, and start the new `server.py` in the background (detached), ensuring it logs to `/home/user/logs/server.log`.

5. **Log Rotation:**
   - Create a logrotate configuration file at `/home/user/logrotate.conf` to manage `/home/user/logs/server.log`.
   - Requirements for the config: rotate daily, keep 3 old copies, compress old copies, missingok, notifempty.
   - Since you don't have root, you will need to specify a local state file when running logrotate.
   - Force run logrotate once using your config and a local state file at `/home/user/logrotate.state` so that it creates at least one rotated log file (e.g. `server.log.1.gz` or similar, depending on how you force it). Hint: You may need to create a dummy log entry first.

**Final Actions:**
1. Make sure `deploy.sh` is executable.
2. Execute `/home/user/deploy.sh` to trigger the first deployment and start the server.
3. Echo "Test log entry" >> `/home/user/logs/server.log`.
4. Run logrotate manually with the `--force` flag using your configuration and state file so that an archive is created in `/home/user/logs/`.