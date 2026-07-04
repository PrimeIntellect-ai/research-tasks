You are acting as a backup operator testing a restoration procedure. We need to verify that a backed-up service can be restored, configured, and monitored correctly without root privileges.

An archive of the service is located at `/home/user/backup.tar.gz`. 

Perform the following steps:
1. Extract the archive into a new directory: `/home/user/restore/`.
2. Inside the extracted files, you will find `server.c`. This is a simple C daemon, but it currently fails to start because it is hardcoded to bind to port 80 (which requires root access). Edit `server.c` to bind to port `8080` instead.
3. Compile the modified `server.c` into an executable named `server` in the `/home/user/restore/` directory using `gcc`.
4. Create a bash script at `/home/user/watchdog.sh` (ensure it is executable). This script must act as a basic process supervisor:
   - It should check if any service is actively listening on `127.0.0.1` port `8080` (e.g., using `nc -z`).
   - If the port is NOT open, the script must start `/home/user/restore/server` in the background.
5. Create a text file at `/home/user/cron.txt` containing exactly one line: the crontab entry required to schedule `/home/user/watchdog.sh` to run every 5 minutes.
6. Execute your `/home/user/watchdog.sh` script once manually. This should start the server.
7. Wait 1-2 seconds, then connect to `127.0.0.1` on port `8080` to retrieve the server's status message. Save the exact output to `/home/user/restore_status.log`.