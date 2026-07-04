You are a deployment engineer tasked with rolling out an update for a legacy Python application without root access. You need to write an idempotent Python deployment script that backs up the old version, provisions TLS certificates, prepares the new application version, and sets up user-space port forwarding.

Your objective is to write a single Python script at `/home/user/deploy.py` that performs the following steps. The script must be completely idempotent (safe to run multiple times without causing errors or overriding generated files unnecessarily).

Requirements for `/home/user/deploy.py`:
1. **Backup Phase**:
   - Check if the archive `/home/user/backups/app_backup.tar.gz` exists.
   - If it does not exist, create the directory `/home/user/backups/`, compress the directory `/home/user/app_v1` into `app_backup.tar.gz`, and append the exact string "BACKUP_CREATED" to `/home/user/deploy.log`.
   - If it does exist, do nothing to the archive and append "BACKUP_EXISTS" to `/home/user/deploy.log`.

2. **TLS Provisioning**:
   - Check if both `/home/user/certs/cert.pem` and `/home/user/certs/key.pem` exist.
   - If they do not exist, create the `/home/user/certs/` directory and use a subprocess calling `openssl` to generate a self-signed RSA 2048-bit certificate valid for 365 days (no passphrase, subject can be anything). Append "CERTS_GENERATED" to `/home/user/deploy.log`.
   - If they do exist, append "CERTS_EXIST" to `/home/user/deploy.log`.

3. **Application Setup**:
   - Create the directory `/home/user/app_v2/`.
   - Inside it, generate a Python script named `/home/user/app_v2/server.py`.
   - The generated `server.py` must be a standalone HTTPS web server using Python's built-in libraries (`http.server`, `ssl`, etc.).
   - It must listen on `127.0.0.1` port `8443` using the certificates generated in step 2.
   - When a `GET` request is made to the path `/status`, it must return an HTTP 200 response with the exact `Content-Type: application/json` and the body: `{"version": "v2", "status": "ok"}`. For any other path, it can return a 404.

4. **Port Forwarding Configuration**:
   - Since we lack root access for `iptables`, we will simulate a firewall port forward.
   - The deployment script must create an executable bash script at `/home/user/forward.sh`.
   - When executed, `/home/user/forward.sh` should run a `socat` command that listens on TCP port `8080` (bound to `127.0.0.1`) and transparently forwards all traffic to `127.0.0.1` port `8443`.

Do not start the server or the forwarder inside `deploy.py`. The automated test will execute `/home/user/deploy.py` twice to verify idempotency and log outputs, and then it will execute `/home/user/app_v2/server.py` and `/home/user/forward.sh` in the background to test the HTTPS endpoint. Ensure `deploy.py` is executable.