You are a systems engineer tasked with diagnosing and fixing a failing systemd service for a Rust-based web application. 

The application is a monitoring agent that provides a TLS-encrypted health check endpoint. It runs entirely in user-space. Currently, the `systemctl --user start health-server.service` command fails, and the server is not reachable.

Here is your diagnostic and remediation mission:

1. **Investigate the Failure:** The service is defined in `/home/user/.config/systemd/user/health-server.service`. It fails to start. Check its logs and configuration.
2. **Mount the Certificates:** The application requires TLS certificates located in `/home/user/app/certs/`. However, the certificates are bundled in an archive at `/home/user/certs.zip`. You must modify the systemd service file to automatically mount this zip archive to `/home/user/app/certs` using `archivemount` *before* the Rust binary runs, and safely unmount it (using `fusermount -u`) when the service stops.
3. **Fix the Rust Code:** 
   - The Rust source code is located at `/home/user/app/health-server`. 
   - There is a configuration error in `/home/user/app/health-server/src/main.rs` causing a permission denial upon binding. Update the code to bind to `127.0.0.1:8443` instead.
   - The `/health` endpoint is unimplemented and returns an error. Modify the endpoint handler in the Rust code to return an HTTP 200 OK status with the exact JSON body: `{"status": "healthy"}`.
4. **Deploy and Start:**
   - Compile the Rust application (using `cargo build --release` or similar).
   - Reload the user systemd daemon and successfully start the `health-server.service`.
5. **Verification:**
   - Ensure the service remains in the `active (running)` state.
   - Execute a curl request to verify the endpoint: `curl -k https://127.0.0.1:8443/health`
   - Save the exact standard output of this curl command to `/home/user/health_output.json`.

Constraints:
- You do not have root (`sudo`) access. Everything must be executed as `user`.
- Do not move or extract the zip file permanently; it must be dynamically mounted by the systemd service.