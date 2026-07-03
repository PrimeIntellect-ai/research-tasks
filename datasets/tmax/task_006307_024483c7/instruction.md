You are a network engineer troubleshooting a connectivity issue in a mock local environment. The environment consists of a local Nginx proxy, a Python web application, and a mock interactive router CLI. 

Your goals are to resolve a 502 Bad Gateway error, automate an interactive router login, set up process supervision for the web app, and implement a backup script based on a mock mount configuration.

Perform the following tasks:

1. **Fix the Nginx 502 Error:**
   - There is an Nginx configuration file located at `/home/user/nginx/nginx.conf`. It configures a server listening on `127.0.0.1:8080`.
   - Nginx currently returns a 502 error because its upstream is pointing to an incorrect Unix domain socket path (`/tmp/wrong.sock`).
   - Modify `/home/user/nginx/nginx.conf` so the upstream points to the correct socket: `/home/user/app.sock`.

2. **Automate Router Configuration (Expect Scripting):**
   - There is a mock interactive router script at `/home/user/router_cli.py`.
   - Write a Python script named `/home/user/auto_login.py` that uses the `pexpect` module to interactively configure the router.
   - The interactive sequence is:
     - Prompt: `Username: ` -> Send: `admin`
     - Prompt: `Password: ` -> Send: `secret`
     - Prompt: `Router> ` -> Send: `enable bgp`
     - Prompt: `Router> ` -> Send: `exit`
   - Run your `/home/user/auto_login.py` script. (If successful, the router script will create a file at `/home/user/bgp_enabled.log`).

3. **Process Supervision:**
   - The upstream web application is located at `/home/user/webapp.py`.
   - Write a Python script named `/home/user/supervisor.py` that spawns `python3 /home/user/webapp.py` as a subprocess.
   - The supervisor must continuously monitor the child process. If the child process exits or crashes, the supervisor must immediately restart it.
   - The supervisor script must write its own PID to `/home/user/supervisor.pid` when it starts, and run indefinitely in the background.
   - Start your `/home/user/supervisor.py` script in the background. Ensure the web application socket (`/home/user/app.sock`) is created.

4. **Backup Strategy based on Fstab:**
   - There is a mock fstab file at `/home/user/fake_fstab`.
   - Write a Python script named `/home/user/backup.py` that parses `/home/user/fake_fstab` to find the mount point associated with the device `backup_drive`.
   - The script should create this mount point directory if it does not exist.
   - The script should then create a gzipped tarball of the `/home/user/nginx/` directory and save it to the backup mount point as `nginx_backup.tar.gz`.
   - Run your `/home/user/backup.py` script.

5. **Verification:**
   - Start Nginx in the background using your modified configuration:
     `nginx -c /home/user/nginx/nginx.conf -p /home/user/nginx/`
   - Make a GET request to `http://127.0.0.1:8080` using `curl` and redirect the output to `/home/user/curl_result.log`. The output should be the successful response from the web application.

Ensure all scripts are executable if needed, and paths are exactly as specified. Do not use sudo or require root privileges.