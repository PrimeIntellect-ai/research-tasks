You are an engineer tasked with fixing a broken supervision script that simulates a cron job environment. 

Currently, there is a job scheduler simulation script at `/home/user/run_task.sh` that periodically executes a monitoring script (`/home/user/supervisor/monitor.py`). Because `run_task.sh` strips all environment variables (like a highly restrictive `cron` environment), `monitor.py` is failing. Worse, due to how relative paths are handled, it is writing its error logs to the wrong location, and the SSH tunnel it is supposed to maintain is not starting.

Your objective is to diagnose and fix the configuration, update the process manager, define the SSH tunneling parameters, and implement an email alert script.

Perform the following fixes:

1. **Fix the Process Supervisor (`monitor.py`)**:
   - The script `/home/user/supervisor/monitor.py` currently attempts to execute `ssh_manager.sh`, but fails because it assumes the script is in the system `PATH` or current directory. Modify `monitor.py` to use the absolute path `/home/user/supervisor/ssh_manager.sh`.
   - Update the exception handling in `monitor.py`: if an error occurs, it currently appends to `error.log` in the current working directory. Change it so it explicitly appends to `/home/user/logs/monitor_error.log`.
   - On a successful execution of the SSH manager, `monitor.py` must execute a new Ruby script at `/home/user/supervisor/alert.rb` before exiting.

2. **Configure the SSH Tunnel (`ssh_manager.sh`)**:
   - Edit `/home/user/supervisor/ssh_manager.sh`.
   - Instead of actually establishing an SSH connection (which would hang or fail without credentials), update the script to simply append the exact SSH port forwarding command to a log file at `/home/user/logs/ssh_cmd.log`, and then `exit 0`.
   - The command you must log should set up a local port forward running in the background, without executing a remote command. Specifically, it must forward local port `8080` to `localhost:80` on the remote server `mockuser@remotehost`. Use the standard `ssh` flags for backgrounding (`-f`) and not executing a command (`-N`). The logged string should be exactly: `ssh -f -N -L 8080:localhost:80 mockuser@remotehost`.

3. **Implement the Email Alert (`alert.rb`)**:
   - Create a Ruby script at `/home/user/supervisor/alert.rb` (ensure it has executable permissions).
   - When run, this script must create a correctly formatted email spool file at `/home/user/mail/alert.eml`.
   - The contents of `/home/user/mail/alert.eml` must be EXACTLY:
     ```
     To: admin@example.com
     Subject: Tunnel Restored
     
     Tunnel is active.
     ```

4. **Verify Your Fix**:
   - Run `/home/user/run_task.sh`.
   - Ensure that the execution completes without errors, `/home/user/logs/ssh_cmd.log` contains the correct SSH command, and `/home/user/mail/alert.eml` is generated.
   - Finally, write a file at `/home/user/success.txt` containing the word `DONE`.