You are tasked with fixing a malfunctioning backup system for a server. There is a Python script that acts as our periodic backup job, but it is writing logs to the wrong directory due to working directory differences when invoked, its timestamps are in the wrong timezone, and it crashes because it lacks permissions to write to the secure backup location.

Your objective is to fix the Python script, configure the correct permissions, set up log rotation, and correctly configure the local timezone handling within the script.

Here are the detailed requirements:

1. **Initial Setup Requirements** (You must create these directories and files to simulate the environment):
   - Create the directory `/home/user/data/` and a file `/home/user/data/source.txt` containing the text: `critical system data`.
   - Create the directory `/home/user/secure_backup/`.
   - Create the directory `/home/user/app_logs/`.

2. **Permission Management**:
   - The `/home/user/secure_backup/` directory must have exact permissions `750` (rwxr-x---).

3. **The Backup Script (`/home/user/backup_job.py`)**:
   Create a Python script at `/home/user/backup_job.py` that performs the following:
   - **Timezone**: The script must forcefully set its own timezone to `Europe/Berlin` at runtime (using `os.environ` and `time.tzset()`) so that all Python logs use this timezone regardless of system settings.
   - **Logging & Rotation**: Configure Python's built-in `logging` module to use a `RotatingFileHandler`.
     - The log file MUST strictly be written to the absolute path `/home/user/app_logs/backup.log` (fixing the issue where it wrote to the wrong location based on the current working directory).
     - Set `maxBytes=60` and `backupCount=3`.
     - The log format must be exactly: `%(asctime)s - %(message)s`
   - **File Operation**: The script must read `/home/user/data/source.txt` and append its contents to `/home/user/secure_backup/archive.txt`. Add a newline after each append.
   - **Logging Action**: After appending the file, the script must log exactly this message: `Backup successful`

4. **Execution**:
   - Run your script `/home/user/backup_job.py` exactly **10 times** in a row. Because of the `maxBytes=60` limit, this will trigger the `RotatingFileHandler` to rotate the logs multiple times.

5. **Verification Artifact**:
   - Once completed, run `ls -la /home/user/app_logs/ > /home/user/final_listing.txt`.
   - Ensure that `/home/user/app_logs/backup.log` and its rotated backups (e.g., `backup.log.1`, etc.) exist.