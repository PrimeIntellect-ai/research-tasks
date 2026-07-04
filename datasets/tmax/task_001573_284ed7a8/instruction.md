You are a Linux systems engineer tasked with hardening and deploying a user-space mock mailing list processing pipeline. We are running in an unprivileged container, so you cannot use systemd or root access. Instead, you will use `supervisord` to manage the daemon, implement a backup step, use text processing to sanitize emails, and perform a staged deployment.

Your goal is to complete the following pipeline in `/home/user`:

1. **Directories**: Ensure the following directories exist:
   - `/home/user/mail/incoming`
   - `/home/user/mail/sanitized`
   - `/home/user/mail/processed`
   - `/home/user/mail/backup`

2. **Text Processing (Sanitization)**:
   Write a bash script at `/home/user/sanitize.sh`. This script must:
   - Read all `.eml` files in `/home/user/mail/incoming/`.
   - Use `sed` or `grep`/`awk` to entirely remove any line starting with exactly `X-Internal-Route:` (case-sensitive) from the files.
   - Save the cleaned files with the same filenames into `/home/user/mail/sanitized/`.
   - Ensure the script is executable.

3. **Backup Strategy**:
   Write a Python script at `/home/user/backup_mail.py`. This script must:
   - Archive the entire contents of `/home/user/mail/incoming/` into a single zip file located at `/home/user/mail/backup/backup_current.zip`.

4. **Mail Processor Daemon (Python)**:
   Write a Python script at `/home/user/processor_v2.py`. This script acts as a long-running daemon:
   - It should continuously monitor `/home/user/mail/sanitized/` (e.g., using a simple loop with `time.sleep(1)`).
   - For every `.eml` file it finds, it must read the content, append a new line containing exactly `Status: Processed` at the end of the file.
   - It must then move the modified file to `/home/user/mail/processed/` (keeping the original filename).
   - Ensure the script flushes standard output if it prints anything.

5. **Service Management (Supervisord)**:
   Create a supervisord configuration file at `/home/user/supervisord.conf`.
   - It must configure a program called `mail_processor`.
   - The command for this program must execute a symlink located at `/home/user/current_processor.py` using `python3`.
   - Configure it to write stdout to `/home/user/mail_processor.log`.
   - Include the `[supervisord]` and `[rpcinterface:supervisor]` sections necessary to run it in user space (e.g., pidfile at `/home/user/supervisord.pid`, socket or port for supervisorctl).

6. **Rolling Deployment Script**:
   Write a bash script at `/home/user/deploy.sh` that orchestrates the deployment:
   - Executes `/home/user/backup_mail.py`.
   - Executes `/home/user/sanitize.sh`.
   - Creates or updates a symlink at `/home/user/current_processor.py` to point to `/home/user/processor_v2.py`.
   - Starts supervisord using the configuration file you created (`supervisord -c /home/user/supervisord.conf`).
   - Sleeps for 5 seconds to allow the daemon to process the files.
   - Creates a final verification file at `/home/user/deploy_success.log` containing the text `DEPLOYMENT COMPLETE`.

Once you have created all necessary files, execute `/home/user/deploy.sh`.