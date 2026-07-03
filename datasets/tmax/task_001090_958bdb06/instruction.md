You are a backup operator testing a disaster recovery restore for a custom metrics pipeline. The system consists of a C++ metrics daemon and a testing script, but the restored configuration contains hardcoded paths from the old environment. Like an Nginx 502 bad gateway caused by a wrong upstream socket path, our test script is failing to communicate with the daemon.

Your task is to fix the restored C++ code, compile it, set up port forwarding to bridge legacy and new systems, and configure log rotation for the daemon's output.

Here are the specific requirements:

1. **Extract the backup:**
   Extract `/home/user/backup_archive.tar.gz` into the directory `/home/user/restore/`.

2. **Fix and Compile the C++ Daemon:**
   Inside the extracted files, you will find `metrics_daemon.cpp`. It currently listens on an obsolete UNIX socket path (`/home/user/old.sock`).
   Modify the C++ source code so it listens on `/home/user/app.sock`.
   Compile the fixed source code using `g++` into an executable named `metrics_daemon` in the `/home/user/restore/` directory.

3. **Configure Log Rotation:**
   The daemon writes its output to `/home/user/app_metrics.log`.
   Create a logrotate configuration file at `/home/user/logrotate.conf` to manage this log file. The configuration must include the following directives specifically for `/home/user/app_metrics.log`:
   - Rotate hourly (`hourly`)
   - Keep 5 backups (`rotate 5`)
   - Compress old log files (`compress`)
   - Ignore missing log files (`missingok`)

4. **Establish Port Forwarding:**
   The provided test script (`/home/user/restore/send_test.sh`) is hardcoded to send legacy metric payloads to a TCP port (localhost, port 9999). 
   You must set up a port forward that listens on TCP port 9999 and forwards all traffic to the daemon's new UNIX socket (`/home/user/app.sock`). You can use `socat` to accomplish this.

5. **Execute the End-to-End Test:**
   - Start the compiled `metrics_daemon` in the background.
   - Start your `socat` port forwarding process in the background.
   - Wait 1-2 seconds for the listeners to bind.
   - Execute the test script: `/home/user/restore/send_test.sh`. This will send a test payload over TCP, which should be forwarded to the UNIX socket and logged by the daemon.
   - Wait 2 seconds for the daemon to flush the logs, then cleanly kill both the `socat` and `metrics_daemon` processes.

6. **Verification File:**
   Once everything is successfully tested and logs are written, create an empty file at `/home/user/task_done.txt` to indicate you are finished.