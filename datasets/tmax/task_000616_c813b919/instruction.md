You are tasked with fixing and completing a custom user account management system for our site administrators. The system consists of multiple cooperating services located in `/app/`:

1. **The SMTP Relay (Running):** A mock SMTP server is already running on `127.0.0.1:2525`. It saves all received emails to `/app/mail_spool/`.
2. **The Account Report Daemon (Broken C Program):** Located at `/app/account_daemon.c`. This program is supposed to listen on TCP port `8888`. When it receives a line like `REPORT <username>\n`, it must execute `/app/generate_report.sh <username>` to get the user's account summary. It should then send an email containing this summary to `admin@local.site` via the SMTP relay on `127.0.0.1:2525`. Currently, the C program is incomplete and has syntax errors. You must fix it, compile it to `/app/account_daemon`, and run it in the background.
3. **The Report Script (Broken Bash Script):** Located at `/app/generate_report.sh`. It must use `awk`, `sed`, or `grep` to extract the user's home directory from `/app/passwd` (which follows the standard `/etc/passwd` format). It must output EXACTLY: `User <username> has home <homedir>`. Currently, the text processing pipeline is broken.
4. **The Scheduled Backup (Broken Environment):** A background process continuously runs `/app/cron_backup.sh` every 5 seconds to back up user logs. However, because it runs in a restricted environment, the `BACKUP_DIR` variable is empty, causing it to write backups to `/tmp/` instead of the correct location: `/app/backups/`. Fix `/app/cron_backup.sh` so that it explicitly resolves and writes to `/app/backups/` regardless of the caller's `PATH` or environment variables.
5. **Log Rotation:** Create a script at `/app/rotate_logs.sh` that takes a file path as an argument. When run, it should rename the file by appending `.1` (e.g., `activity.log` becomes `activity.log.1`), and create a new empty file in its place with permissions `644`.

Your objectives:
- Fix `/app/generate_report.sh` so it accurately extracts the home directory from `/app/passwd`.
- Fix, compile, and start `/app/account_daemon.c` so it binds to `127.0.0.1:8888`. Upon receiving `REPORT <username>\n`, it must send an SMTP message. The SMTP message must have the envelope sender `daemon@local.site`, recipient `admin@local.site`, and the email body must exactly match the output of `generate_report.sh`. 
- Fix `/app/cron_backup.sh` so backups actually appear in `/app/backups/`.
- Create the `/app/rotate_logs.sh` script as specified.

Ensure all services are running and the backups are successfully accumulating in `/app/backups/`.