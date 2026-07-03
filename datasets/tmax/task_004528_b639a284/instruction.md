You are acting as a backup operator testing a disaster recovery procedure. Our custom C-based application multiplexer needs to be restored from a backup, reconfigured for the local test environment, and verified.

Your tasks are as follows:

1. **Extract the Backup:** 
   Extract the archive located at `/home/user/archive/multiplexer_backup.tar.gz` into the directory `/home/user/restore/`. 

2. **Fix the Upstream Socket Configuration:**
   The restored configuration file at `/home/user/restore/config.ini` contains production settings. The application routes requests to an upstream UNIX socket. Currently, it points to `/var/run/backend.sock`. Change this upstream path in the config file to point to `/home/user/backend_service/app.sock`.

3. **Application-Level User Administration:**
   The multiplexer performs its own internal access control (acting as an application firewall) based on a flat file. Add the user `backup_operator` to `/home/user/restore/allowed_users.db` so that your test queries will not be rejected. The format of the file is one username per line.

4. **Process Supervision & Mock Backend:**
   Create a bash script at `/home/user/backend_service/run_backend.sh`. This script must act as a process supervisor for a mock backend. 
   It should use `socat` or `nc` to listen on the UNIX socket `/home/user/backend_service/app.sock`. 
   Whenever a connection is made, it should reply with the string `RESTORE_VALID\n`.
   Critically, the script must contain a loop to automatically restart the socket listener immediately if it exits or crashes, ensuring continuous availability. Run this supervisor script in the background.

5. **Fix the C Source Code (Timezone/Locale Bug):**
   The multiplexer source code is at `/home/user/restore/src/multiplexer.c`. There is a bug where the application validates a hardcoded license expiration date using `mktime()`, but it fails because it relies on the system's local timezone, which differs in this test environment.
   Modify `multiplexer.c` to explicitly set the `TZ` environment variable to `UTC` (using `setenv("TZ", "UTC", 1);`) right at the beginning of the `main()` function, ensuring the date validation passes.

6. **Compile and Test:**
   Compile the C program:
   `gcc /home/user/restore/src/multiplexer.c -o /home/user/restore/multiplexer`
   
   Start the multiplexer in the background. It reads `config.ini` by default.
   Once running, the multiplexer listens on `127.0.0.1:8080`. Send a TCP payload to this port containing the username followed by a colon and the request payload (e.g., `backup_operator:PING`). 
   Capture the exact response received from the multiplexer (which forwards to your mock backend) and save it to `/home/user/restore_success.log`.

Ensure all background processes are running and the log file contains the expected backend response at the end of your interaction.