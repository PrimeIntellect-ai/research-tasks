You are a backup operator. We need to automate the testing of our application backup restores to ensure they are valid and our configurations can be dynamically adapted to a staging environment.

You have been provided a backup archive at `/home/user/backups/archive.tar.gz`.

Your goal is to extract this backup, write tools to modify its configuration for staging, create a service manager to run it, and perform a health check to validate the restore. 

Perform the following steps:
1. Extract `/home/user/backups/archive.tar.gz` into the directory `/home/user/staging/`. (Create the directory if it doesn't exist).
2. Inside the extracted files, there is a configuration file at `etc/app.conf`. Using text processing tools or a script of your choice, modify the extracted `etc/app.conf` in place so that:
   - `listen_port` is changed from its original value to `8080`
   - `db_path` is changed from its original value to `/home/user/staging/data/db.sqlite`
3. Write a service lifecycle management script at `/home/user/manager.sh` that accepts one argument: `start`, `stop`, or `status`.
   - `start`: Executes the extracted binary `/home/user/staging/bin/app_mock` in the background, passing the absolute path to `etc/app.conf` as its only argument. It must save the Process ID (PID) to `/home/user/staging/app.pid`.
   - `stop`: Reads the PID from `/home/user/staging/app.pid`, kills the process, and removes the PID file.
   - `status`: Checks if the process in the PID file is currently running. If running, exit with code 0; if not, exit with code 1.
   Make sure `/home/user/manager.sh` is executable.
4. Start the service using your manager script.
5. Write a monitoring script at `/home/user/health_check.sh` (in any language) that reads `etc/app.conf`, verifies the mock application is running (using `manager.sh status`), and generates a final report at `/home/user/restore_report.log` with exactly the following format:
   ```
   [STATUS] RUNNING
   [PORT] <the extracted listen_port value>
   [DB] <the extracted db_path value>
   [RESULT] RESTORE VALID
   ```
   If the status check fails, the `[RESULT]` should be `RESTORE INVALID`.
6. Run `/home/user/health_check.sh` so the log file is generated.

Do not use root/sudo privileges. Ensure all paths used are absolute paths in your scripts where necessary.