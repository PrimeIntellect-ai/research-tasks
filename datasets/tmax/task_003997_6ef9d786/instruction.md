You are a Linux systems engineer tasked with hardening and automating the deployment of a legacy interactive C daemon. The source code for this daemon is located at `/home/user/src/interactive_daemon.c`.

Your goal is to compile the daemon, automate its interactive login using `expect`, wrap the execution in a bash script that sets up the required environment, and configure log rotation for its output.

Perform the following steps:

1. **Compilation**: Compile `/home/user/src/interactive_daemon.c` into an executable named `/home/user/bin/interactive_daemon`.

2. **Environment Setup**: The daemon strictly requires an environment variable `DAEMON_ENV` to be set to `hardened` to run. Add the appropriate export command to `/home/user/.bashrc` so that any interactive shell sets this variable.

3. **Automation Script**: The daemon interactively prompts for a PIN on standard input with the exact string: `Enter Hardening PIN: `.
   Create an Expect script at `/home/user/bin/auto_start.exp` that spawns the executable `/home/user/bin/interactive_daemon`, waits for the prompt, and securely sends the PIN `7924` followed by a newline. Make sure it allows the spawned process to continue running indefinitely (e.g., using `interact` or a continuous loop, but since it's a daemon, keep the expect process alive to pass through the output).

4. **Wrapper Script**: Create a Bash wrapper script at `/home/user/bin/launch.sh` that does the following:
   - Sources `/home/user/.bashrc` to ensure `DAEMON_ENV` is present in the environment.
   - Executes the Expect script (`/home/user/bin/auto_start.exp`).
   - Redirects all standard output and standard error from the Expect script to `/home/user/daemon_logs/app.log`.
   Ensure the script is executable.

5. **Log Rotation**: Create a logrotate configuration file at `/home/user/daemon_logrotate.conf` specifically for `/home/user/daemon_logs/app.log`. It must apply the following directives:
   - Rotate daily
   - Keep exactly 4 rotations (backups)
   - Compress the rotated logs
   - Ignore missing log files (`missingok`)
   - Do not rotate if the log is empty (`notifempty`)

6. **Execution**: Start the wrapper script in the background (for example, using `nohup /home/user/bin/launch.sh &`) and let it run for at least 3 seconds so that the daemon has time to initialize, accept the PIN, and write to the log file.

Leave the daemon running in the background when you complete the task.