You are tasked with deploying a custom Python-based process supervisor and log backup system. As a system administrator, you must handle an unstable application, manage its logs, and route backups based on a system configuration file. 

You need to write a robust Python script `/home/user/supervisor.py` that does the following:

1. **Process Supervision**: 
   - Start the executable Python script `/home/user/flappy.py` as a subprocess.
   - Redirect the stdout and stderr of this subprocess to `/home/user/logs/flappy.log`.
   - Monitor the subprocess. `flappy.py` is unstable and will occasionally crash (exit with a non-zero status). Whenever it crashes, your supervisor must catch the failure, log an internal message (e.g., "Process crashed, restarting..."), and immediately restart the process.

2. **Log Configuration & Rotation**:
   - The supervisor must continually monitor the size of `/home/user/logs/flappy.log`.
   - Implement a log rotation mechanism directly in your supervisor script: when `flappy.log` exceeds 1024 bytes (1 KB), rotate it. 
   - Keep up to 3 old logs (`flappy.log.1`, `flappy.log.2`, `flappy.log.3`). 

3. **Fstab Parsing & Archiving**:
   - Parse the file `/home/user/fstab_mock`. Look for the entry corresponding to the device `/dev/mapper/backup_vol`. Extract its designated mount point.
   - Ensure this mount point directory exists.
   - Every time a log is rotated, immediately copy the newly rotated `flappy.log.1` into this backup mount point directory. Name the copied file `backup_[TIMESTAMP].log` (e.g., `backup_1680000000.log`).

4. **Execution and Shutdown**:
   - The supervisor should run for exactly 20 seconds and then gracefully terminate `flappy.py` and exit itself.
   - Finally, your script must generate a report at `/home/user/summary.txt` in the following format:
     ```
     Restarts: <number_of_times_flappy_restarted>
     Backups: <number_of_files_in_the_backup_directory>
     Backup_Dir: <absolute_path_parsed_from_fstab>
     ```

**Environment Requirements:**
- All directories (like `/home/user/logs`) should be created by your script if they don't exist.
- Use Python 3. You may write standard bash scripts to run your python program if you wish, but the supervisor logic must be in Python.
- Do not use root/sudo commands.