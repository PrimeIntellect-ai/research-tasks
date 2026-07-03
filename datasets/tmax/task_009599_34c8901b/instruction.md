You are an operator testing the restore processes for our infrastructure. As part of this, we run a local monitoring daemon that listens for restore-completion events. However, the restore environment is unprivileged, and the daemon is currently failing to bind because its socket path is hardcoded to a root-owned directory.

Your task is to fix the C code for the daemon, set up the correct environment variable for it, compile it, and schedule it via cron.

Here are the specific steps:

1. **Extract Configuration:** We have a configuration file at `/home/user/config/backup_vars.conf` that contains various properties. Find the value of `SOCKET_PATH` in this file. 
2. **Fix the C Code:** Open the source code for the monitoring daemon at `/home/user/src/restore_monitor.c`. You will notice the `sun_path` for the Unix domain socket is hardcoded to `/var/run/restore.sock`. 
   Modify this C code so that instead of using the hardcoded string, it reads the socket path from the `MONITOR_SOCK` environment variable using `getenv("MONITOR_SOCK")`. Make sure to handle the case where the environment variable is not set (e.g., exit with code 1).
3. **Compile:** Compile the modified C code using `gcc`. Place the compiled executable at `/home/user/bin/restore_monitor`.
4. **Environment Setup:** Add an `export` statement to `/home/user/.bash_profile` that sets the `MONITOR_SOCK` environment variable to the exact path you found in the `backup_vars.conf` file.
5. **Schedule:** Add a cron job for the current user that executes `/home/user/bin/restore_monitor` every 5 minutes. (The cron expression should be `*/5 * * * *`). 
6. **Verification File:** Dump your configured crontab to a file at `/home/user/cron_backup.txt` using `crontab -l > /home/user/cron_backup.txt`.

Ensure all files are created in the exact paths specified.