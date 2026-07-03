You are assisting a network engineer in setting up a local monitoring daemon to troubleshoot intermittent connectivity to an internal SMTP relay. Since you do not have root access, you will build user-space tools and configurations to achieve this.

Please complete the following steps:

1. **Email User/Group Administration via Aliases:**
   There is a mail alias file located at `/home/user/mail_aliases.txt`. The format is `group_name: user1, user2`.
   Create a new Rust project at `/home/user/smtp_monitor`. Write a Rust program (in `src/main.rs`) that first reads this file. If the `net-admins` group does not include the user `alice`, the program must append `, alice` to that group's list and write the changes back to `/home/user/mail_aliases.txt`.

2. **Network Monitoring & Logging:**
   After updating the aliases, the Rust program should attempt to establish a TCP connection to `127.0.0.1:2525` with a 1-second timeout.
   - It should perform exactly 3 attempts, pausing for 100 milliseconds between each attempt.
   - Append the result of each attempt to `/home/user/logs/smtp_monitor.log`. Write exactly `CONNECT_OK\n` if successful, or `CONNECT_FAIL\n` if it fails.
   - Exit with status code `1` if all attempts failed, or `0` if at least one succeeded.

3. **Log Rotation Configuration:**
   Create a standard `logrotate` configuration file at `/home/user/logrotate.conf` specifically for `/home/user/logs/smtp_monitor.log`. Set the following policies:
   - Rotate when the file size exceeds `10 bytes` (using the `size` directive).
   - Keep exactly `3` rotated backups.
   - Compress the rotated logs.
   - Use the `missingok` and `nomail` directives.

4. **Process Supervision:**
   Create a bash script at `/home/user/supervisor.sh` that acts as a simple process supervisor for your compiled Rust binary (`/home/user/smtp_monitor/target/debug/smtp_monitor`).
   - The script should run the binary.
   - If the binary exits with a non-zero exit code (e.g., failed to connect), the supervisor should sleep for 1 second and restart it.
   - If the binary exits with code 0, the supervisor should gracefully terminate itself with exit code 0.
   - Make the script executable.

Ensure the Rust project compiles successfully and all files are placed in their exact specified absolute paths.