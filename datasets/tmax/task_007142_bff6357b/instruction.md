You are a system administrator responsible for setting up the deployment configuration for a new internal Python-based microservice. Because you do not have root access on this development environment, you will prepare the deployment files, set up local mock data, and test the server code locally.

Please complete the following tasks:

1. **User & Group Mock Administration**
   Create a Python script at `/home/user/setup_users.py`. This script must create an SQLite3 database at `/home/user/data/users.db`.
   - The database must contain a table named `users` with columns: `id` (INTEGER PRIMARY KEY), `username` (TEXT), and `group_name` (TEXT).
   - The script must insert two records:
     - username: `webadmin`, group_name: `wheel`
     - username: `mailer`, group_name: `mail`
   - Run the script so the database is created.

2. **Web Server Setup & TLS Configuration**
   - Generate a self-signed RSA TLS certificate (2048-bit) and private key. Place them at `/home/user/tls/cert.pem` and `/home/user/tls/key.pem`. Set the Common Name (CN) to `localhost`.
   - Write a Python web server script at `/home/user/web/app.py`. The server should use Python's built-in `http.server` and `ssl` modules to serve over HTTPS.
   - It must listen on `127.0.0.1:9443` and use the certificate and key you generated.
   - For any `GET` request to the root path (`/`), it must return a `200 OK` status with the exact JSON payload: `{"status": "ok"}` and the `Content-Type: application/json` header.

3. **Container Lifecycle Management (Configuration)**
   Create a `Dockerfile` at `/home/user/web/Dockerfile` that containerizes this application. The `Dockerfile` must:
   - Use `python:3.10-slim` as the base image.
   - Create a non-root user named `appuser` and switch to it using the `USER` instruction.
   - Copy `app.py` into `/app/`.
   - Expose port `9443`.
   - Set the command to run `app.py`.

4. **Verification**
   - Start your Python web server (`/home/user/web/app.py`) in the background.
   - Run a `curl` command against `https://127.0.0.1:9443/` (ensure you pass the appropriate flag to allow/verify the self-signed cert).
   - Save the exact standard output of this `curl` command to `/home/user/verification.log`.

Make sure all directories (`/home/user/data`, `/home/user/tls`, `/home/user/web`) are created before writing files to them.