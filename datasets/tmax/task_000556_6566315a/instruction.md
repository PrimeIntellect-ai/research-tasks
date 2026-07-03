We are dealing with a red-team operator who has been crafting sophisticated evasion payloads targeting our file upload handler, which was recently found susceptible to path traversal. We need you to secure our upload architecture, which consists of three services: an Nginx reverse proxy, a Flask API, and an internal SFTP server.

Your task is to fix the environment, configure the services, and build a robust path-traversal sanitizer to stop the evasion payloads.

Step 1: Multi-Service Integration
The setup script in `/app/setup.sh` has installed the necessary packages, but the services are not properly glued together.
- Nginx is listening on port 8080 but its configuration at `/etc/nginx/sites-available/default` is empty. Configure it to proxy requests from `/api/` to the Flask service.
- The Flask service runs on port 5000. It receives file uploads. You must modify `/app/flask/app.py` to require and validate a standard JWT Bearer token (secret: `redteam_hunter_99`) in the `Authorization` header before accepting uploads.
- The Flask service must use SSH/SFTP to save the uploaded files to the local SFTP server running on port 2222. Generate an SSH keypair for the user `flask_svc`, configure the SFTP server to trust it, and update `app.py` to use this key for authentication.

Step 2: Network Security
Implement local firewall rules (using `iptables`) so that:
- Port 8080 is accessible from anywhere.
- Port 5000 (Flask) is ONLY accessible from localhost (Nginx).
- Port 2222 (SFTP) is ONLY accessible from localhost (Flask).
Drop all other inbound traffic. Save your rules to `/home/user/firewall_rules.v4`.

Step 3: Adversarial Payload Sanitizer
We have captured the red-team's evasion payloads and stored them in `/app/corpora/evil/` (containing filenames and paths used for path traversal, e.g., `....//`, null bytes, URL encoded variants). Standard benign uploads are in `/app/corpora/clean/`.
Write a Python script at `/home/user/sanitizer.py` with the following CLI signature:
`python3 /home/user/sanitizer.py --filename <name> --path <target_dir>`
The script must print "SAFE" to stdout if the input is benign, and "EVIL" if it detects any path traversal attempt. You must integrate this script into `app.py` to reject malicious uploads with a 403 status code.

Ensure the end-to-end flow works: a client uploading a file with a valid JWT through Nginx (port 8080) successfully drops the file into the SFTP backend, provided the filename passes your sanitizer.