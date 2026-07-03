You are a monitoring specialist tasked with setting up a local, user-space alert pipeline. You need to create a custom monitoring script, configure environment variables, set up a local mock email server, and write a simple process supervisor to keep your services running. 

Because you do not have root access, you will configure everything in `/home/user`.

Here are your requirements:

1. **Environment Configuration**:
   Create a file at `/home/user/.monitor_profile` that exports two variables:
   - `ALERT_THRESHOLD=90`
   - `ALERT_EMAIL=admin@local.dev`

2. **Monitoring Script**:
   Create a script at `/home/user/monitor.py` (you can use Python or Bash) that runs in a continuous loop checking the file `/home/user/cpu.txt` every 1 second.
   - If the file does not exist, assume the value is 0.
   - If the integer value inside `/home/user/cpu.txt` is strictly greater than the `ALERT_THRESHOLD` environment variable, it must send an email to `ALERT_EMAIL` from `monitor@local.dev` with the subject "CPU Alert" and the body "Threshold exceeded".
   - It should send this email via SMTP to `127.0.0.1` on port `10025`.
   - To prevent spam, once an alert is sent, the script should not send another alert until the value drops to `ALERT_THRESHOLD` or below and then exceeds it again.

3. **Mock SMTP Server**:
   Create a simple script or command that runs a mock SMTP server on `127.0.0.1:10025`. Any emails received by this server must be appended to `/home/user/email_out.log` in plain text. 

4. **Process Supervisor**:
   Create a bash script at `/home/user/supervisor.sh` that:
   - Sources `/home/user/.monitor_profile`.
   - Starts the mock SMTP server in the background.
   - Starts `monitor.py` in the background.
   - Continuously monitors the `monitor.py` process. If `monitor.py` crashes or exits for any reason, the supervisor must automatically restart it within 2 seconds.

**Initial State**:
Before starting your supervisor, run:
`echo 50 > /home/user/cpu.txt`

**Final Action**:
Make sure your scripts are executable. Run your supervisor script in the background (`/home/user/supervisor.sh &`) so it is actively monitoring `/home/user/cpu.txt` and handling restarts before you complete the task.