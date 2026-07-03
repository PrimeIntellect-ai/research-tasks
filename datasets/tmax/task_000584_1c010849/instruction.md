You are a monitoring specialist tasked with setting up a lightweight, secure alert ingestion and backup system. 

You must perform the following steps:

1. **Environment Setup**:
   - Create the directories `/home/user/alerts`, `/home/user/backups`, `/home/user/src`, `/home/user/bin`, and `/home/user/certs`.
   - Add the following environment variables to `/home/user/.bashrc`:
     - `ALERT_DIR=/home/user/alerts`
     - `ALERT_PORT=8080`
   - Ensure these variables are loaded in your current session.

2. **Alert Daemon (C Programming)**:
   - Write a C program in `/home/user/src/alert_daemon.c`.
   - The program must read the `ALERT_PORT` and `ALERT_DIR` environment variables.
   - It should listen for incoming TCP connections on `localhost` at the port specified by `ALERT_PORT`.
   - When a client connects and sends the exact string "TRIGGER\n" (followed by a newline), the daemon must append the string "ALERT_FIRED\n" to the file `$ALERT_DIR/alerts.log`.
   - The daemon should reply to the client with "OK\n" and close the connection.
   - The daemon must handle multiple consecutive connections (looping to accept new ones) but does not need to handle concurrent connections (a simple single-threaded accept loop is fine).
   - Compile the program to `/home/user/bin/alert_daemon`.

3. **Secure Log Serving (TLS Setup)**:
   - Generate a self-signed RSA 2048-bit certificate and unencrypted private key in `/home/user/certs/` named `server.crt` and `server.key`. The subject can be anything.
   - Write a shell script `/home/user/serve_logs.sh` that, when executed, uses `openssl s_server` to listen on port `8443` using the generated certificate and key, and serves the content of `$ALERT_DIR/alerts.log`. It should close the connection after sending the file (e.g., using standard `openssl s_server` flags for a single file serve or HTTP mock). Specifically, the script should start the server in the background.

4. **Backup Strategy**:
   - Write a bash script `/home/user/backup.sh` that creates a tar.gz archive of `$ALERT_DIR/alerts.log`.
   - The archive should be saved in `/home/user/backups/` and named `alerts_backup.tar.gz`.

5. **Execution & Verification**:
   - Start the `/home/user/bin/alert_daemon` in the background.
   - Simulate an alert by sending "TRIGGER\n" to localhost:8080 (e.g., using `nc` or `echo`).
   - Run `/home/user/backup.sh` to generate the backup archive.
   - Leave the daemon running.