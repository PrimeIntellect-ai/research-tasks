You are an observability engineer tuning the backend data collection for a new internal dashboard. Your team relies on Git for configuration management, and you need to build a set of tools to capture Git events and handle email-based alerts, feeding all of this into dashboard logs.

Since our team standardizes on Rust, you must write the core components in Rust. You have a standard Linux environment (Ubuntu-based) without root privileges. Cargo and rustc are already installed.

Complete the following objectives:

1. **Dashboard Directories**:
   Create the directory `/home/user/dashboard/` to store our logs.

2. **Git Hook (Rust)**:
   Initialize a bare Git repository at `/home/user/metrics-config.git`.
   Write and compile a `post-receive` Git hook in Rust for this repository. 
   When a user pushes to this repository, the hook must read the standard input (which Git provides as `oldrev newrev refname`) and append a strictly formatted JSON line to `/home/user/dashboard/events.log`.
   The JSON line must look exactly like this:
   `{"type": "push", "ref": "<refname>"}`
   (e.g., `{"type": "push", "ref": "refs/heads/main"}`). Make sure the hook binary is placed in the correct location and is executable.

3. **Mock SMTP Daemon (Rust)**:
   Write a Rust program named `smtp-alerter` and compile it. 
   This program must act as a simple background TCP daemon listening on `127.0.0.1:8025`.
   When a client connects and sends text, the daemon must read the incoming lines. If it encounters a line starting with `Subject: `, it must extract the rest of the line (excluding the `Subject: ` prefix and any trailing whitespace/newlines) and append it as a raw string to `/home/user/dashboard/alerts.log`, followed by a newline.
   The daemon must stay running and accept multiple connections (handling them sequentially is fine).
   Start this daemon in the background.

4. **Process Monitoring & Scheduled Task**:
   We need to ensure `smtp-alerter` stays running.
   Write a bash script at `/home/user/monitor.sh` that checks if the `smtp-alerter` process is running. If it is not running, the script must start it in the background.
   Configure the current user's crontab to run `/home/user/monitor.sh` every minute.

Ensure all code is compiled, the daemon is running, the cron job is installed, and the Git repository is fully ready to accept local pushes.