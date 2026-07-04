You are an operations engineer tasked with diagnosing and fixing a custom deployment script that acts as a simple container lifecycle manager. 

We have a script at `/home/user/manager.sh` that is designed to set up a deployment directory, link in static assets, and start a Python-based TLS web server. However, the script is currently failing to serve files properly. It suffers from issues similar to cron jobs executing in unexpected contexts: relative paths are resolving incorrectly, and the required TLS certificates are missing entirely.

Here is the current state of the system:
- A static website is located at `/home/user/static_files/`. It contains a single file, `index.html`.
- The supervisor script is at `/home/user/manager.sh`.
- The web server logic is provided in `/home/user/server.py`.

Your objectives are to fix the script and get the application running:

1. **Generate TLS Certificates**: 
   Create a self-signed certificate and private key in the directory `/home/user/certs/`. Name them `cert.pem` and `key.pem` respectively. (Use no passphrase).

2. **Fix Directory Structure and Symlinks**:
   Modify `/home/user/manager.sh`. The script currently attempts to symlink the static files into the "container" directory (`/home/user/containers/app1/www`), but the symlink target is broken because of relative path misunderstanding. Fix the `ln` command in `manager.sh` so that `/home/user/containers/app1/www` correctly points to `/home/user/static_files`.

3. **Fix the Web Server Launch Command**:
   The `server.py` script requires a port, a certificate file, and a key file as arguments. `manager.sh` currently passes incorrect, unresolved paths to these certificates. Modify `manager.sh` so that it provides the correct absolute paths to the `cert.pem` and `key.pem` you created, ensuring the server successfully starts. 
   The server MUST be started such that its working directory is `/home/user/containers/app1/www` so it serves the correct files.

4. **Deploy and Verify**:
   - Run `/home/user/manager.sh start app1` to deploy the application.
   - Wait a couple of seconds for the server to bind to port 8443.
   - Execute a `curl` command to fetch the `index.html` file securely (ignoring self-signed cert warnings) from `https://localhost:8443/index.html` and save the exact output to `/home/user/verification.txt`.

Do not modify `/home/user/server.py` or `/home/user/static_files/index.html`. You only need to write commands to generate the certs, edit `/home/user/manager.sh`, start the service, and verify it.