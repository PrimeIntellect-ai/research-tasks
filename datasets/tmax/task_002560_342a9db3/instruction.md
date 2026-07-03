You are a backup operator testing a user-space restore simulation process. Because we do not have root privileges, we simulate mounts and container lifecycles using Python scripts.

Your task is to write a Python script at `/home/user/run_restore.py` that orchestrates a simulated restore and manages a mock container process. 

The script must perform the following actions:
1. **Fstab-like parsing:** Read the file `/home/user/user_backup.fstab`. This file mimics `/etc/fstab` with space-separated columns: `<source_dir> <dest_dir> <type> <options> <dump> <pass>`. 
2. **Simulate Bind Mounts:** For each entry in the fstab file:
   - If the `<source_dir>` does not exist, silently ignore the entry and move to the next one (do not log an error or raise an exception).
   - If it exists, create the `<dest_dir>` if it doesn't already exist.
   - For every file in the `<source_dir>`, create a symbolic link to it inside the `<dest_dir>` (simulating a read-only bind mount).
3. **Container Lifecycle Management & Log Rotation:** 
   - Spawn a subprocess running `/home/user/mock_container.py` (use the current python interpreter). Pass the successfully "mounted" `<dest_dir>` paths as positional arguments to the script.
   - Capture the standard output of this subprocess.
   - Write the captured output to `/home/user/restore_process.log`. Because the mock container is extremely verbose, you must configure log rotation *within your Python script* using `logging.handlers.RotatingFileHandler`.
   - Set the rotation policy to a maximum file size of `1024` bytes, keeping exactly `2` backups (`backupCount=2`).
4. **Cleanup:**
   - Let the subprocess run for exactly `2.0` seconds.
   - Terminate the subprocess cleanly using `SIGTERM`.
   - Wait for the subprocess to finish terminating before your script exits.

Ensure your script is executable or runnable via `python3 /home/user/run_restore.py`. You only need to provide the `run_restore.py` script and run it once so the final log files and symlinks are generated.