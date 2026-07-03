You are a monitoring specialist investigating frequent 502 errors caused by a missing upstream application socket. You need to create an automated alert script and prepare a filesystem configuration to permanently fix the underlying mount issue. 

Your tasks are:

1. **Create a Monitoring Script**: Write a Python 3 script at `/home/user/monitor.py` that checks for the existence of the application socket file located at `/home/user/run/app.sock`. 
   - If the file *does not* exist, the script must send an alert email.
   - The email must be sent via an unauthenticated SMTP server listening locally on `localhost` port `8025`.
   - The sender email must be `monitor@local`.
   - The recipient email must be `admin@local`.
   - The email Subject must be exactly: `Alert: Socket Missing`.
   - The email Body must be exactly: `Error at <timestamp>`, where `<timestamp>` is the current time localized to the `Europe/Berlin` timezone.
   - The timestamp format must be exactly `YYYY-MM-DD HH:MM:SS` (e.g., `2024-10-24 14:30:00`). Use the standard library `zoneinfo` module.
   - If the socket file *does* exist, the script should exit cleanly without sending an email.

2. **Prepare Mount Configuration**: The root cause of the missing socket is that the application writes to an alternate directory, which isn't mounted to the run path. Prepare the fstab configuration to fix this.
   - Create a file at `/home/user/fstab_entry.txt`.
   - In this file, write the single `/etc/fstab` line required to bind-mount the directory `/home/user/app_data/run` to `/home/user/run`.
   - Use standard bind mount syntax (e.g., fstype `none`, options `bind`, and standard dump/pass values of `0 0`).

Do not run an SMTP server yourself; assume the testing environment will start one on port 8025 to verify your Python script. Ensure your Python code is executable or cleanly runnable via `python3 /home/user/monitor.py`.