You are an engineer tasked with diagnosing and fixing a custom backup service written in Go. The service is supposed to run in the background, serving a backup archive of a specific directory over a secure HTTPS connection. However, the service currently fails to start and does not securely serve the files.

Here is the situation:
1. The service source code is located at `/home/user/service/backup_daemon.go`. It is supposed to serve an on-the-fly tarball of `/home/user/important_data` on port `8443`.
2. The service is failing because it is configured to use standard HTTP instead of HTTPS, and it lacks the necessary TLS certificates.

Your objectives:
1. **Fix the Go Service and TLS Configuration:**
   - Create a directory `/home/user/service/certs`.
   - Generate a self-signed TLS certificate (`cert.pem`) and private key (`key.pem`) inside `/home/user/service/certs`. Use RSA 2048-bit and a validity of 365 days.
   - Modify `/home/user/service/backup_daemon.go` to use HTTPS (`ListenAndServeTLS`) on port `8443`, pointing to the certificates you just generated. 
   - Compile the fixed Go code into a binary named `backup_daemon` in `/home/user/service/`.
   - Run the binary in the background.

2. **Establish a Secure Tunnel Command:**
   - To securely access this backup service from a remote backup server, we use SSH local port forwarding.
   - Write the exact SSH command that would forward local port `9443` on the client to `localhost:8443` on the server, running in the background without executing remote commands. Connect as `user@localhost`.
   - Save this single SSH command as a string inside a file named `/home/user/tunnel_cmd.sh`.

3. **Verify and Restore the Backup:**
   - Use `curl` to securely download the backup from your running Go service over `https://localhost:8443` (ignoring self-signed certificate warnings).
   - Save the downloaded archive to `/home/user/backup_verified.tar.gz`.
   - Extract the contents of `/home/user/backup_verified.tar.gz` into the directory `/home/user/restored_data/`.

Ensure all steps are completed and the restored data matches the original `important_data`.