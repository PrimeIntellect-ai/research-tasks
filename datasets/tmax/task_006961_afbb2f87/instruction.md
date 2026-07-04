You are acting as a backup operator testing a restore of our custom C-based Mailing List Delivery Agent (MDA) and its backend configuration service.

We have a backup archive located at `/home/user/mda_backup.tar.gz`. 
Your objective is to extract the backup, compile the MDA application, and successfully start the service stack to verify the restored data.

However, the provided startup script has a known race condition mimicking a missing systemd `After=` dependency: it attempts to start the C-based MDA immediately after launching the backend configuration service, but the backend takes a few seconds to initialize and bind to its port (9050). Because the MDA does not have built-in retry logic, it crashes on startup if the port is not yet open.

Perform the following steps:
1. Extract `/home/user/mda_backup.tar.gz` into the directory `/home/user/restore/`.
2. Compile the C source code found at `/home/user/restore/src/mailer.c` into an executable located at `/home/user/restore/bin/mailer`. (You will need to create the `bin` directory).
3. Inspect and modify the shell script `/home/user/restore/start_all.sh`. You must fix the race condition using bash scripting (e.g., by adding a polling loop that checks if `localhost` port `9050` is accepting connections before executing the `mailer` binary).
4. Run your modified `/home/user/restore/start_all.sh`. 

When the `mailer` successfully connects to the backend service, it will process the mock mailing list backup and automatically generate a log file at `/home/user/success.log`. 

The automated test will verify the success of your task solely by checking for the existence and correct contents of `/home/user/success.log`.