You are tasked with securing and repairing a custom configuration orchestrator that manages Nginx routing manifests. Recently, malicious users submitted configurations that caused widespread 502 Bad Gateway errors by manipulating upstream socket paths, and we need to lock down the system.

You must complete the following four objectives:

**1. Incident Video Analysis**
A recording of the Nginx error log during the incident has been provided at `/app/incident_logs.mp4`. Using `ffmpeg` and any necessary text extraction tools (like `tesseract-ocr`, which you can install locally or use string extraction if applicable), analyze the video. 
Find the exact number of times the string "502 Bad Gateway" is clearly visible in the frames.
Write this exact integer to `/home/user/502_count.txt`.

**2. Idempotent Backup Restoration**
We have a known-good backup of the Nginx configuration directory at `/home/user/nginx_backup.tar.gz`.
Write a script at `/home/user/restore_nginx.sh` that idempotently restores this backup into `/home/user/nginx_conf/`.
- If `/home/user/nginx_conf/` already exists, it should safely clear out the old contents and restore the fresh ones.
- The script must ensure all `.conf` files inside `/home/user/nginx_conf/` have `0644` permissions.

**3. Manifest Filter (Adversarial Validator)**
Users submit routing manifests in YAML format. We must reject malicious ones.
Create an executable script (in any language, but you must ensure it runs directly, e.g., `/home/user/validator.py` or `/home/user/validator.sh`).
It will be invoked as: `<your_script> <path_to_yaml_file>`
- Exit code `0`: The manifest is CLEAN.
- Exit code `1`: The manifest is EVIL.

*Rules for a CLEAN manifest:*
- Must be valid YAML.
- Must contain `kind: Upstream`.
- Under `spec.socket`, the path must start exactly with `/var/run/app/` and end with `.sock`.
- The socket filename must only contain alphanumeric characters, hyphens, and underscores before the `.sock` extension.

*Rules for an EVIL manifest:*
- Any manifest containing path traversal (e.g., `../`).
- Any manifest pointing to paths outside `/var/run/app/` (e.g., `/etc/passwd`, `/var/run/app_backup/`).
- Any manifest with shell metacharacters in the socket path (e.g., `;`, `|`, `&`, `$`).
- Missing `spec.socket` or `kind: Upstream`.

We have provided two directories for your own testing:
- `/app/corpus/clean/` (contains examples of clean manifests)
- `/app/corpus/evil/` (contains examples of malicious manifests)
*Note: The automated test will use a hidden holdout set of clean and evil manifests.*

**4. Expect Script for Email Alerting**
A local raw SMTP server is running on `127.0.0.1` port `2525`.
Write an `expect` script at `/home/user/send_alert.exp` that connects to this port using `telnet` or `nc` and simulates an interactive SMTP session to send an email.
- The `MAIL FROM` must be `system@orchestrator.local`.
- The `RCPT TO` must be `admin@orchestrator.local`.
- The `DATA` must contain the subject `Subject: Validator Deployed` and the body `The manifest validator is now active.`
- The expect script must gracefully handle the SMTP server's responses (like `250 OK` and `354 End data with <CR><LF>.<CR><LF>`) and issue the `QUIT` command.