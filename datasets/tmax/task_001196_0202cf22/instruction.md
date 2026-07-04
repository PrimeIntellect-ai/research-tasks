You are a site administrator tasked with building an automated deployment script to process new user accounts, update local configuration files, and synchronize them with a legacy Identity Provider (IdP). 

The legacy IdP only accepts connections on port 8000 and is restricted. You must securely route traffic to it via an SSH tunnel.

Your objective is to create an automated deployment and processing pipeline. 

Requirements:

1. **Directories & Files**:
   - Incoming user requests are stored in `/home/user/requests/`. Each file is named `<username>.txt` and contains a single line specifying their role, for example: `role: editor`.
   - You must create an archive directory at `/home/user/archive/`.
   - You must update the site's configuration file located at `/home/user/config/site_users.ini`.

2. **Configuration File Management**:
   - The `/home/user/config/site_users.ini` file does not exist yet. 
   - Your automation must create it, ensure the first line is exactly `[Users]`, and append each processed user in the format `username=role` (e.g., `alice=editor`).

3. **Automation Script**:
   - Write a processing script in any language of your choice (e.g., Python, Bash, Node.js).
   - For every `.txt` file in `/home/user/requests/`:
     1. Parse the username from the filename and the role from the file content.
     2. Update `/home/user/config/site_users.ini` as described above.
     3. Send an HTTP POST request to `http://127.0.0.1:9090/sync` with a JSON body formatted exactly as: `{"username": "<username>", "role": "<role>"}` and header `Content-Type: application/json`.
     4. Move the successfully processed `.txt` file to `/home/user/archive/`.

4. **Deployment & SSH Tunneling**:
   - SSH key authentication for `user@localhost` is already configured.
   - Create a master bash script at `/home/user/deploy.sh`.
   - The `deploy.sh` script must:
     1. Establish a local SSH port forward running in the background. It should map local port `9090` to `localhost:8000` (the legacy IdP) using `user@localhost`.
     2. Wait a few seconds to ensure the tunnel is active.
     3. Execute your automation processing script.
     4. Gracefully terminate the background SSH tunnel process after the automation script finishes.
   - Ensure `deploy.sh` has executable permissions.

5. **Execution**:
   - Run your `/home/user/deploy.sh` script to process the existing requests and verify your pipeline works.