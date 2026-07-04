You are an infrastructure engineer automating our new provisioning environment. We are migrating away from a legacy system where our automated cron jobs frequently failed or wrote logs to the wrong locations due to PATH environment differences.

We have a legacy stripped and packed binary at `/app/legacy_prov_hash`. We lost the source code for this binary. It takes a single string argument and prints a calculated provisioning token. 
Your primary task is to write a replacement script located exactly at `/home/user/new_prov_hash.py` that behaves bit-for-bit identically to `/app/legacy_prov_hash` for any ASCII string input containing alphanumeric characters, dashes, and underscores. The script must take the input string as its first command-line argument and print only the resulting token to standard output.

Once you have your replacement script, you need to set up the rest of the automated provisioning environment:

1. **Git Hook Configuration:**
   - Create a bare git repository at `/home/user/provision_repo.git`.
   - Create a `post-receive` hook in this repository. Whenever code is pushed, the hook must read the ref updates. For each pushed ref, it should extract the pushed branch name (e.g., `main` or `feature-1`), pass it to your `/home/user/new_prov_hash.py` script to generate a token, and append a line to `/home/user/logs/provision.log`.
   - The log line format must be strictly: `[<TIMESTAMP>] BRANCH:<branch_name> TOKEN:<generated_token>`, where timestamp is in standard ISO 8601 format (e.g., `2023-10-25T14:30:00Z`).
   - Ensure the hook uses absolute paths for everything to avoid the previous PATH issues.

2. **Log Configuration and Rotation:**
   - Create a logrotate configuration file at `/home/user/logrotate.conf` to rotate `/home/user/logs/provision.log` daily, retaining exactly 5 backups. Uncompressed.
   - Install a user-level cron job that runs this logrotate configuration every day at midnight. Explicitly define the PATH at the top of the crontab to avoid the historical legacy issues we faced.

3. **Web Server Setup & TLS:**
   - Serve the `/home/user/logs/` directory over HTTPS using Nginx running entirely in user-space (no root required).
   - Generate a self-signed TLS certificate and key at `/home/user/tls/cert.pem` and `/home/user/tls/key.pem`.
   - Configure Nginx to listen on port 8443 and serve the directory index for `/home/user/logs/`.
   - The Nginx configuration file must be located at `/home/user/nginx.conf`, and Nginx must be started in the background using this configuration. Store its PID in `/home/user/nginx.pid`.

Make sure to test your `new_prov_hash.py` thoroughly against the legacy binary to ensure it matches exactly!