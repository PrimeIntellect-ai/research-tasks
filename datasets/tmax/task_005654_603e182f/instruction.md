You are a monitoring specialist tasked with building a secure, supervised filesystem alerting mechanism. We need to monitor a specific data drop directory and expose the alert logs securely. 

Since you do not have root privileges, you must set everything up within `/home/user` and use user-space tools for supervision, port forwarding, and serving.

Please complete the following setup:

1. **Directories**: Create the following directories if they don't exist:
   - `/home/user/src`
   - `/home/user/bin`
   - `/home/user/data_drop`
   - `/home/user/alerts`
   - `/home/user/certs`

2. **C++ Filesystem Monitor**:
   Write a C++ program at `/home/user/src/monitor.cpp`.
   - The program must use Linux `inotify` to watch the `/home/user/data_drop` directory for newly created files (`IN_CREATE` event).
   - It should ignore any files that do not end with the `.dat` extension.
   - When a `.dat` file is created, append exactly this JSON string to `/home/user/alerts/alerts.log` on a new line:
     `{"alert": "new_data", "file": "<filename>"}` (where `<filename>` is the exact name of the file created, e.g., `report.dat`).
   - The program must flush the file stream after writing to ensure real-time logging.
   - It should run continuously in the foreground.

3. **CI/CD Build Script**:
   Write a shell script at `/home/user/deploy.sh` that compiles `/home/user/src/monitor.cpp` using `g++` and outputs the executable to `/home/user/bin/fs_monitor`. Ensure the script has execute permissions and run it to build the binary.

4. **Web Server & TLS**:
   - Generate a self-signed RSA certificate (`cert.pem`) and private key (`key.pem`) in `/home/user/certs/` without a passphrase.
   - Write a Python 3 script at `/home/user/server.py` that serves the contents of the `/home/user/alerts/` directory over HTTPS. It must bind to `127.0.0.1` on port `8443` and use the generated TLS certificates.

5. **Port Forwarding**:
   - Because standard firewall rules require root, use `socat` to create a local port forward. TCP traffic coming into `127.0.0.1:9090` should be forwarded to the secure Python server at `127.0.0.1:8443`.

6. **Process Supervision**:
   - Write a `supervisord` configuration file at `/home/user/supervisord.conf`.
   - It must run as the current user and supervise three programs:
     1. `fs_monitor`: Running `/home/user/bin/fs_monitor`
     2. `https_server`: Running `/usr/bin/env python3 /home/user/server.py`
     3. `port_forward`: Running the `socat` port forwarding command.
   - Ensure `supervisord` is configured to output its own logs to `/home/user/supervisord.log` and a PID file to `/home/user/supervisord.pid`.

7. **Activation**:
   - Start your `supervisord` instance using `supervisord -c /home/user/supervisord.conf`. 
   - Ensure all three supervised processes are in the `RUNNING` state.

Do not ask for further information. You must implement, build, configure, and start the entire pipeline described above.