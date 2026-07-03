You are acting as a backup operator testing the restoration of a critical internal Python service. A backup archive has been placed at `/home/user/backup.tar.gz`. 

Your objective is to extract, configure, verify, and launch the restored service. Follow these exact steps:

1. **Extraction and Permissions:**
   Extract `/home/user/backup.tar.gz` into the directory `/home/user/restored_app`. 
   The archive contains an environment file named `.env`. For security reasons, change its permissions so that ONLY the owner has read and write access (no permissions for group or others).

2. **Data Integrity Verification (Text Processing):**
   The archive also contains a log file named `restore_data.log`. Write a Python script at `/home/user/check_logs.py` that reads `/home/user/restored_app/restore_data.log` and counts the exact number of lines containing the uppercase word `CORRUPT`. 
   Your Python script must output ONLY this integer to a file located at `/home/user/corrupt_count.txt`. Run this script.

3. **Process Supervision and Port Forwarding Simulation:**
   The application requires a local port forwarder. Instead of SSH, we will use a Python background process. 
   The restored app contains a script `/home/user/restored_app/server.py`. 
   Create a bash script at `/home/user/supervise.sh` that implements a process supervision loop. The script must:
   - Run `python3 /home/user/restored_app/server.py`
   - If `server.py` crashes or exits, the loop should immediately restart it.
   - Run this `supervise.sh` script in the background.
   - Save the Process ID (PID) of the running `supervise.sh` bash process to `/home/user/supervisor.pid`.

Ensure all requested files (`/home/user/corrupt_count.txt`, `/home/user/supervisor.pid`) are created and have the correct contents before finishing.