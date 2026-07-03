You are an infrastructure engineer setting up an automated deployment and notification pipeline on a single Linux machine. You will be using systemd user services, Python, and Git. You do not have root access.

Your goal is to set up a workflow where pushing to a local Git repository triggers a webhook service. This service then creates a backup of a directory and sends a notification email via a local SMTP sink.

Here are the specific requirements:

1. **SMTP Sink Service:**
   - Create a Python script at `/home/user/smtp_sink.py` that listens for incoming SMTP connections on `127.0.0.1:8025`.
   - When an email is received, the script must save the raw email content (headers and body) as a `.eml` file in the directory `/home/user/emails/` (you will need to create this directory). The filename should be `<timestamp>.eml`.
   - Configure this script to run as a systemd user service named `smtp-sink.service`. Enable and start it.

2. **Git Repository and Hook:**
   - Initialize a bare Git repository at `/home/user/project.git`.
   - Create a `post-receive` hook in this repository.
   - The hook must make an HTTP POST request to `http://127.0.0.1:8080/deploy`.

3. **Webhook Notifier Service (Vendored Package):**
   - We have provided a pre-packaged source directory at `/app/webhook-notifier-1.0.0`.
   - This package contains a Python HTTP server (`server.py`) and a systemd unit file (`webhook-notifier.service`).
   - The Python code has a deliberate bug related to how it handles the `SMTP_PORT` environment variable when connecting to the SMTP server. You must find and fix this bug.
   - The `webhook-notifier.service` file is missing the appropriate systemd directives to ensure it starts *after* `smtp-sink.service` and requires it to be running. Add the correct `After=` and `Requires=` (or `Wants=`) directives.
   - The webhook service expects the `BACKUP_DIR` environment variable to be `/home/user/backups/` (create this directory) and the `SOURCE_DIR` to be `/home/user/project.git`.
   - Install the fixed service as a systemd user service, enable, and start it. It should listen on `127.0.0.1:8080`.

Ensure both services (`smtp-sink.service` and `webhook-notifier.service`) are active and running without errors.

When the setup is complete, an automated verification script will simulate a git push to `/home/user/project.git`. The pipeline should successfully execute, resulting in a backup tarball in `/home/user/backups/` and an email in `/home/user/emails/`.