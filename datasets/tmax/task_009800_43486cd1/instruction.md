You are an infrastructure engineer building a local provisioning automation tool. We are simulating a service environment where dependencies must be ordered correctly (e.g., configuring TLS, starting a service, then updating firewall/group configs). Since you do not have root access, we will use local files to simulate system configurations.

Your task is to write and execute a Go program at `/home/user/provision.go` that performs the following steps in order:

1. **TLS Configuration:**
   Idempotently generate a self-signed TLS certificate and private key in the `/home/user/certs` directory. The files must be named `cert.pem` and `key.pem`. If they already exist, do not regenerate them. Use any standard tool (like `openssl`) by executing it from within your Go code, or use Go's standard library.

2. **Web Server Setup:**
   Start a simple HTTPS server on port `8443` using the generated `cert.pem` and `key.pem`. 
   - The server must respond to `GET /health` with the exact plaintext body `OK`.
   - Run this server in the background (e.g., via a goroutine) so your script can continue.

3. **Service Dependency Check (The "After=" simulation):**
   Your script must actively poll `https://127.0.0.1:8443/health` (ignoring TLS certificate verification errors since it is self-signed) until it receives the `OK` response, proving the server is up, before proceeding to the configuration steps below.

4. **User Group Administration (Mock):**
   Idempotently update the mock group file located at `/home/user/app-groups.conf`. 
   The file contains colon-separated values: `group_name:password:gid:user_list`.
   You must ensure the user `deployer` is added to the `web-admin` group's user list (comma-separated). If `deployer` is already in the list, do nothing. Do not modify other groups.

5. **Firewall Rules (Mock):**
   Idempotently update the mock firewall configuration located at `/home/user/fw-rules.json`.
   The file contains a JSON array of rule objects. You must ensure an object exactly matching `{"port": 8443, "action": "allow"}` exists in the array. If it doesn't, append it.

6. **Completion Logging:**
   Once all the above steps are completed successfully, append the exact line `Provisioning complete: server reachable` to `/home/user/provision.log`.

Write the script, run it, and leave the Go script running (or make it pause/wait at the end) so that the background web server remains active on port 8443 for verification.