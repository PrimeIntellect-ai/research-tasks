You are a Cloud Architect migrating a legacy C-based microservice to a new infrastructure. We are putting this backend service behind a reverse proxy. However, the migration is currently failing: the proxy simulator reports a "502 Bad Gateway" (connection refused) because the backend is listening on the wrong UNIX domain socket path. 

Before making changes, you must back up the source code, fix the configuration in the code, compile and manage the daemon process, and verify logging functionality.

Here is your step-by-step task:

1. **Backup Strategy**: 
   The legacy source code is located at `/home/user/migration/src`. Create a compressed tarball backup of this directory and save it exactly as `/home/user/migration/backup/src_backup.tar.gz`.

2. **Network/Socket Configuration**: 
   Inspect and modify the C source file at `/home/user/migration/src/server.c`. 
   Currently, it hardcodes a legacy UNIX socket path. Update the C code so that it binds to the new expected path: `/home/user/migration/socket/backend.sock`.

3. **Compilation & Process Control**:
   Compile the updated `server.c` and output the binary to `/home/user/migration/bin/backend_daemon`. 
   Start the compiled binary as a background process. Save the precise Process ID (PID) of this running daemon into the file `/home/user/migration/daemon.pid`.

4. **Verification**:
   Simulate the reverse proxy by issuing an HTTP GET request to your new UNIX socket using `curl`. 
   Command to simulate the proxy: `curl -s --unix-socket /home/user/migration/socket/backend.sock http://localhost/`
   Save the exact standard output (the response body) of this `curl` command to `/home/user/migration/test_response.txt`.

5. **Storage / Log Monitoring**:
   The C daemon automatically writes to `/home/user/migration/logs/app.log` when it starts and handles requests.
   Write a shell script at `/home/user/migration/monitor.sh` that checks if the file `/home/user/migration/logs/app.log` has a file size strictly greater than 0 bytes. If it does, the script should write the string `Log Active` to `/home/user/migration/status.txt`. 
   Execute your `monitor.sh` script once after completing the curl request.

All necessary directories inside `/home/user/migration/` (src, backup, socket, bin, logs) already exist. The C file `server.c` is already present.