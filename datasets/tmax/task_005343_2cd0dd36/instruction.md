You are a backup operator automating the testing of database restores. The current restore script often fails due to simulated network timeouts during test initialization, similar to a disconnected Docker Compose network. 

We have a flaky bash script located at `/home/user/run_restore.sh`. Your task is to write a Python-based process supervisor and configure it to run on a schedule.

**Step 1: The Supervisor Script**
Write a Python script at `/home/user/supervisor.py` that supervises the execution of `/home/user/run_restore.sh`. 
Your script must meet the following requirements:
1. Parse the configuration file at `/home/user/restore_config.ini`. This file uses standard INI format. Extract the integer value `max_retries` from the `[Settings]` section.
2. Execute `/home/user/run_restore.sh` using the `subprocess` module.
3. If the script exits with code `0`, append `[SUCCESS] Restore completed` to `/home/user/supervisor.log` and exit successfully.
4. If the script exits with a non-zero code, it has failed. Append `[RETRY] Restore failed, attempt X of Y` to `/home/user/supervisor.log` (where X is the current attempt number starting at 1, and Y is the `max_retries` value). Then, wait exactly 1 second and execute the script again.
5. If the script fails `max_retries` times consecutively, append `[FATAL] Restore failed after Y attempts` to `/home/user/supervisor.log` and exit the Python script with a non-zero exit code.

**Step 2: Scheduling**
To ensure the restore tests run continuously, create a file named `/home/user/restore_cron` containing a single crontab line that schedules `/usr/bin/env python3 /home/user/supervisor.py` to run every minute.

Ensure your Python script is executable. You can assume `/home/user/restore_config.ini` and `/home/user/run_restore.sh` already exist.