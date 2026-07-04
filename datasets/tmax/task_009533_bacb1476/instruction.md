I need help fixing and completing my local microservices configuration. I've been trying to set up a local reverse proxy for my mock services, but my network configuration is wrong, and I'm missing some required environment variables and automation.

I have a Git repository at `/home/user/microservices-config`. Inside, there is an Nginx configuration file `nginx.conf` meant to run as an unprivileged user. 

Please perform the following tasks:

1. **Reverse Proxy Configuration**: 
   Edit `/home/user/microservices-config/nginx.conf`. It is currently configured to route traffic for `/auth` and `/data` to the wrong ports. Update the `proxy_pass` directives so that requests to `/auth` route to `http://127.0.0.1:8081` and requests to `/data` route to `http://127.0.0.1:8082`. Leave the listen port as 8080.

2. **Environment Variables**:
   My services require two environment variables to function properly. Add the following to the end of my `/home/user/.bashrc` file so they are loaded in new shells:
   - `AUTH_SECRET` set to `"supersecret"`
   - `DATA_DIR` set to `"/home/user/data"`

3. **Git Pre-commit Hook**:
   I want to ensure no bad configurations are committed. Create a Git pre-commit hook in the repository (`/home/user/microservices-config`) that automatically executes the script `/home/user/microservices-config/validate.sh` before allowing a commit. Make sure the hook script is executable.

4. **Backup Schedule**:
   I have a backup script at `/home/user/backup.sh`. I need to schedule this to run via cron every day at exactly 2:00 AM. Since the cron daemon might not be active in this environment, simply write the standard crontab schedule line (e.g., `* * * * * /path/to/script`) into a new file at `/home/user/cron_schedule.txt`.

Please execute these changes directly in the terminal.