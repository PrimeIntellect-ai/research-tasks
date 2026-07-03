You are a backup operator tasked with testing the restore process of a web server configuration and creating an automated log rotation script based on the restored configuration.

A backup archive of the server's state has been placed at `/home/user/backups/server_state.tar.gz`.

Your task is to:
1. Extract the contents of `/home/user/backups/server_state.tar.gz` into the directory `/home/user/restore_area/` (you must create this directory first).
2. Inside the extracted files, you will find a configuration file at `etc/app_config.conf`. 
3. Create a bash script at `/home/user/bin/rotate_and_test.sh` (create the `/home/user/bin` directory if it does not exist) that performs the following automated actions when run:
   - Parses the `PORT` from the restored `etc/app_config.conf`.
   - Simulates a log rotation for the restored web server by taking the `LOG_DIR` specified in the config, prepending `/home/user/restore_area/` to it, and compressing `access.log` found in that directory into `access.log.1.gz`. It must then empty (truncate) the original `access.log` file.
   - Extracts the `TLS_CERT` path from the config, prepends `/home/user/restore_area/` to it, and checks if the certificate file actually exists.
   - Writes a summary report of the test to `/home/user/restore_summary.txt` in the exact format shown below.

Execute your script once to generate the report and perform the log rotation.

The `/home/user/restore_summary.txt` file must contain exactly these lines (with the dynamic values filled in):
RESTORED_PORT=<port_number>
TLS_CERT_FOUND=<true/false>
LOG_ROTATED=<true/false>

Ensure your script has executable permissions. You must rely purely on bash built-ins, standard coreutils (like `tar`, `gzip`, `grep`, `awk`, etc.) to accomplish this task.