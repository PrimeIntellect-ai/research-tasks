You are a Linux Systems Engineer tasked with deploying a hardened configuration retrieval service. A legacy system was compromised, and we must stand up a secure, temporary C++ backend fronted by a containerized reverse proxy. 

A scanned sticky note containing the vault's authorization passcode has been saved to `/app/secret_passcode.png`. 

Your objective is to complete the following multi-stage workflow:

1. **Environment Configuration**
   - Set the system timezone to `Europe/Helsinki`.
   - Generate and set the system locale to `fi_FI.UTF-8`.

2. **Filesystem and Data Setup**
   - Create a directory `/home/user/secure_fs`.
   - Inside it, create a file named `vault.txt` containing exactly the string: `CONFIDENTIAL_SYSTEM_DATA`
   - Use OCR (e.g., `tesseract`) to extract the alphanumeric passcode from `/app/secret_passcode.png`.

3. **C++ Backend Implementation**
   - Write and compile a C++ HTTP server at `/home/user/server.cpp` (compile to `/home/user/server`).
   - The server must listen on `127.0.0.1:9000` and handle basic `GET /vault` HTTP/1.1 requests.
   - It must require an `Authorization: Bearer <passcode>` header, where `<passcode>` is the exact string you extracted from the image (ignoring trailing whitespace).
   - If the passcode matches, it must read and return the contents of `/home/user/secure_fs/vault.txt` with a `200 OK` status.
   - If the passcode is missing or invalid, return `403 Forbidden`.
   - Run this server in the background.

4. **Network and Tunneling**
   - We must isolate the backend. Create a local SSH tunnel (running in the background) that listens on `127.0.0.1:8080` and forwards all traffic to `127.0.0.1:9000`. You may generate an SSH keypair and authorize it locally to accomplish this without a password.

5. **Containerized Web Server & TLS**
   - Generate a self-signed TLS certificate (`server.crt` and `server.key`) in `/home/user/certs/`.
   - Run an Nginx reverse proxy inside a rootless container (using `podman` or `docker`).
   - The container must listen on `0.0.0.0:8443` (HTTPS).
   - It must terminate TLS using your self-signed certificate and proxy all requests to the SSH tunnel endpoint at `127.0.0.1:8080` on the host. 
   - Ensure the container is running continuously in the background.

Ensure all services are up, running, and properly bound. You have passwordless sudo access if needed for system configuration or installing packages (e.g., `tesseract-ocr`, `podman`, `build-essential`).