You are an AI assistant helping a FinOps analyst optimize cloud storage costs. 

To avoid paying for expensive cloud-native snapshot features on temporary billing reports, the analyst has decided to implement a custom local backup solution using a C program. The program archives files and sends a status report to a local mailing daemon. However, the automated backup service is currently failing.

You have the following environment:
1. A C source file at `/home/user/src/finops_backup.c`. This program checks if the user running it is in the `finops` group, creates a tar archive of `/home/user/billing_reports/` into `/home/user/archives/reports.tar.gz`, and communicates with a local mail socket at `/home/user/run/mailer.sock`.
2. A systemd user service file at `/home/user/.config/systemd/user/finops-backup.service` designed to run the compiled C program.
3. Another systemd user service file at `/home/user/.config/systemd/user/local-mailer.service` which provides the mock mailing socket (`/home/user/run/mailer.sock`).

Your tasks:
1. Compile the C program `/home/user/src/finops_backup.c` into an executable at `/home/user/bin/finops_backup`.
2. Fix the systemd user service `/home/user/.config/systemd/user/finops-backup.service`. It currently fails because it attempts to run before the `local-mailer.service` has initialized the socket. You need to configure it so that it explicitly starts *after* `local-mailer.service` and *requires* it.
3. Reload the systemd user manager and start `finops-backup.service`.
4. Ensure the backup runs successfully.

Verification:
Once successful, the C program will automatically create a log file at `/home/user/logs/backup_success.log` containing the text "FinOps Backup Completed and Notification Sent". The archive `/home/user/archives/reports.tar.gz` must also exist.

You must accomplish this using the provided user account (no `sudo` required).