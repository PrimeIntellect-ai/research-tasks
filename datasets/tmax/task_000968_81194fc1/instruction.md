I need your help fixing my custom user-space CI/CD runner daemon and the C++ project it is trying to build. I am acting as an engineer diagnosing why this service keeps failing to run successfully. 

We have a homemade CI/CD service managed by a bash script at `/home/user/ci_daemon.sh`. It is supposed to:
1. Compile a C++ program located at `/home/user/project/main.cpp`.
2. Run the compiled binary to generate a filtered list of mailing list subscribers.
3. Call a backup script to archive the compiled binary.
4. "Send" a notification email by writing a file to our local mail spool directory.

However, the daemon is failing completely and producing no successful backups or emails. Here is what you need to do to fix the pipeline:

**Step 1: Fix the C++ Application**
The application at `/home/user/project/main.cpp` is a simple program that reads a list of emails from a file (`/home/user/project/emails.txt`), filters out invalid ones (must contain exactly one '@'), and writes the valid ones to `/home/user/project/valid_emails.txt`. Currently, the program has a logical bug that causes it to crash (Segmentation fault) or produce incorrect output. Fix the C++ code so that it successfully compiles with `g++` and correctly filters the emails.

**Step 2: Create the Backup Script**
The daemon expects a backup script at `/home/user/backup.sh`. You must write this script.
- It must be a robust bash script (use `set -e`).
- It should accept exactly one argument: the source directory to backup (which will be `/home/user/project`).
- It must create a compressed tar archive of this directory at `/home/user/backups/project_backup.tar.gz`. (Ensure the `/home/user/backups` directory is created if it doesn't exist).

**Step 3: Fix the CI Daemon Script**
The daemon script at `/home/user/ci_daemon.sh` is broken. 
- It has a syntax error preventing it from running.
- It lacks proper error handling (if the compilation fails, it shouldn't try to run the backup). Fix it so that it exits immediately on any command failure.
- When successful, it should write exactly the text `BUILD SUCCESS` to a simulated email file at `/home/user/mail_spool/notification.txt`. 

**Step 4: Run the Service**
Once you have fixed `main.cpp`, written `backup.sh`, and fixed `ci_daemon.sh`, execute `/home/user/ci_daemon.sh` so that it completes a successful pipeline run.

Verify that:
1. `/home/user/project/valid_emails.txt` exists and contains only the valid emails.
2. `/home/user/backups/project_backup.tar.gz` exists and is a valid tar archive.
3. `/home/user/mail_spool/notification.txt` exists and contains exactly `BUILD SUCCESS`.