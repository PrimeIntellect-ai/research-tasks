You are acting as a Backup Operator testing a disaster recovery scenario for a critical internal application. You have been provided with a backup archive of the application's configuration and identity files, and you need to simulate a restore process, reconstruct the application's required directory structure, set up the necessary environment variables, and write a Python service to validate the integrity of the restored data.

Your tasks are as follows:

1. **Extract the Backup:**
   Extract the archive located at `/home/user/backups/app_backup_latest.tar.gz` into the directory `/home/user/app_restored/`.

2. **Reconstruct Directory and Link Structure:**
   The application expects its active configuration to be available at exactly `/home/user/active_config`. 
   Create a symbolic link at `/home/user/active_config` that points to the restored configuration directory (`/home/user/app_restored/config`).

3. **Environment Setup:**
   Inside the restored config directory, there is a file named `.env`. Create a shell script at `/home/user/setup_env.sh` that, when sourced, exports all the variables defined in this `.env` file. Additionally, append a command to source this script at the end of `/home/user/.bashrc`.

4. **Simulate User and Group Administration (Identity Mapping):**
   Since you do not have root access to recreate system users, the application relies on mock identity files included in the backup (`/home/user/app_restored/system/passwd.mock` and `/home/user/app_restored/system/group.mock`).
   These files follow the standard Linux `/etc/passwd` and `/etc/group` format.
   Write a Python script at `/home/user/map_identities.py` that reads these two files and generates a JSON file at `/home/user/identity_map.json`. The JSON should be a single dictionary where the keys are the usernames (from `passwd.mock`) and the values are their corresponding group names (resolved from `group.mock` using the Primary GID).

5. **Validation Service:**
   Write a Python script at `/home/user/verify_restore.py` that acts as the final validation check. This script must:
   - Verify that the symbolic link `/home/user/active_config` exists and correctly points to `/home/user/app_restored/config`.
   - Read the `identity_map.json` file.
   - Read the environment variable `APP_RESTORE_MODE` (which will be set if your environment setup works and is loaded).
   - Write a final log file at `/home/user/restore_report.json` with the following exact schema:
     ```json
     {
       "config_link_valid": true,
       "app_mode": "<value of APP_RESTORE_MODE>",
       "mapped_users": {
          "username1": "groupname1",
          "username2": "groupname2"
       }
     }
     ```

Run your `verify_restore.py` script so that `/home/user/restore_report.json` is generated. Ensure that the environment variables from the `.env` file are loaded into the shell running the Python script.