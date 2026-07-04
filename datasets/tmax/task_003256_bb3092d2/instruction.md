You are acting as a backup operator testing a staged restore and deployment process. You need to write a Rust script to simulate restoring a specific backup version, deploying it, and rotating the deployment logs. Finally, you will schedule a future automated restore test using `cron`.

Perform the following steps:

1. Create a directory `/home/user/backups` and create two files in it:
   - `/home/user/backups/app_v1.txt` containing the text: `version 1 backup`
   - `/home/user/backups/app_v2.txt` containing the text: `version 2 backup`
2. Create a directory `/home/user/active`.
3. Write a Rust script at `/home/user/deploy_restore.rs` that accepts a single command-line argument representing a version number (e.g., `1` or `2`). The script must do the following:
   - Copy the file `/home/user/backups/app_v<version>.txt` to `/home/user/active/app.txt`.
   - Perform a simple log rotation: If `/home/user/active/deploy.log` exists, rename it to `/home/user/active/deploy.log.old` (overwriting any existing `.old` file).
   - Create a new `/home/user/active/deploy.log` and write the string `Deployed v<version>\n` into it.
4. Compile the Rust script to an executable located at `/home/user/deploy_restore`.
5. Run your compiled executable twice manually to test the rolling deployment and log rotation:
   - First, run it with the argument `1`.
   - Then, run it with the argument `2`.
6. Create a cron configuration file at `/home/user/crontab.txt` that schedules the `/home/user/deploy_restore` executable to run with argument `3` every day at exactly 3:00 AM. 
7. Install this cron configuration using the `crontab` command so that it is actively scheduled for the user.

Ensure your Rust script compiles successfully and handles the file operations cleanly. Do not use absolute paths inside the script unless required, but expect the script to be run from `/home/user`. Use the exact paths and strings mentioned above.