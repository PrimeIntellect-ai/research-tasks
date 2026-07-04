You are an AI assistant helping a site administrator deploy a user account management pipeline on a Linux server.

We have a partially deployed system for syncing user profiles. I need you to complete the setup, fix existing issues, and build a security filter. You only have standard Bash tools, standard CLI utilities, and `tesseract` available. No root access is required (all services are user-level systemd services and Nginx runs as a local unprivileged instance).

Please complete the following steps:

1. **Fix the Backend Service (Systemd Dependency):**
There is a user-level systemd service located at `/home/user/.config/systemd/user/profile-backend.service`. It currently fails to start consistently on boot because it tries to bind to the network before the local stub network service (`stub-net.service`) is fully up. Fix the `profile-backend.service` unit file by adding the correct `After=` dependency. Then, reload the systemd user daemon and start the service.

2. **Retrieve the Port Number via OCR:**
The backend service binds to a specific port, but the developer only left a screenshot of the port configuration at `/app/backend_port.png`. Use `tesseract` (or another tool) to extract the port number from this image. 

3. **Configure the Reverse Proxy:**
Update the Nginx configuration template at `/home/user/deploy/nginx.conf`. Replace the placeholder `{{BACKEND_PORT}}` with the port number you extracted from the image. Check connectivity using `curl` to ensure the proxy successfully routes to the backend on `localhost`.

4. **Create the Adversarial Profile Filter:**
We receive bulk user profile data in JSON format, but some submissions are malicious (e.g., shell injection attempts in the username field). 
Write a Bash script at `/home/user/deploy/filter_profiles.sh` that takes two arguments: an input directory containing JSON files, and an output directory.
The script must:
- Read each `.json` file in the input directory.
- Check the `username` field. If it contains any of the following shell metacharacters: `;&|$\``, it must be considered "evil" and rejected.
- If the username consists only of alphanumeric characters and underscores, it is "clean" and should be processed.
- For clean profiles, create a symbolic link to the original file in the output directory. Do not link or copy the evil profiles.

5. **Schedule the Sync:**
Create a user-level systemd timer (and corresponding service) named `profile-sync.timer` that executes the `/home/user/deploy/filter_profiles.sh` script every 15 minutes. The script should read from `/home/user/incoming_profiles/` and output to `/home/user/public_profiles/`. Ensure both the timer and service are enabled and started.