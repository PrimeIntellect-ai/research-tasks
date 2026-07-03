You are an engineer troubleshooting a locally run C++ data processing daemon that keeps crashing on startup. You have been given a workspace at `/home/user/app/`. 

Inside this directory, you will find:
- `main.cpp`: The source code of the daemon.
- `processor`: The compiled C++ binary of the daemon.
- `data_v1/`: A directory containing an `input.txt` file.

Upon investigating the C++ source code and the daemon's behavior, you realize it is failing to start because it expects a specific directory structure and file linkages that have not been initialized by the deployment system. 

Your task is to fix the environment, verify the application's health, and set up a backup strategy by performing the following steps strictly using the terminal (no root privileges required):

1. **Fix the Directory Structure**: 
   Analyze `main.cpp` to understand what paths it expects. Create a symbolic link in `/home/user/app/` named `current_data` that points to the `data_v1` directory. 
   Once the environment is fixed, run `./processor` in the background. It will automatically create a `status.txt` file in `/home/user/app/` if it successfully initializes.

2. **Setup a Health Check**:
   Create an executable bash script at `/home/user/app/health_check.sh`. This script should check the contents of `/home/user/app/status.txt`. If the file exists and its content is exactly "OK", the script should exit with status code 0. Otherwise, it should exit with status code 1.

3. **Configure a Backup Strategy**:
   Create an executable bash script at `/home/user/app/backup.sh`. This script must create a compressed tarball (`.tar.gz`) of the `/home/user/app/data_v1/` directory and save it as `/home/user/backup/data_backup.tar.gz`. (You will need to create the `/home/user/backup/` directory first).

4. **Schedule the Backup**:
   Write a cron expression that would execute `/home/user/app/backup.sh` at exactly the top of every hour (minute 0). Save ONLY the raw cron job line (e.g., `* * * * * /path/to/script`) into a text file at `/home/user/app/cron.txt`. You do not need to install it into the live crontab, just provide the correct entry in the file.