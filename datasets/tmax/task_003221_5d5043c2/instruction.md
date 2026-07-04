You are a container specialist managing a microservice for a localized mailing list system. As part of the container initialization process, you need an idempotent configuration tool written in C that sets up the mail spool environment and sets the appropriate timezone and locale for the mailing list.

Write a C program at `/home/user/setup_spool.c` and compile it to `/home/user/setup_spool` (using `gcc`).
When executed, `/home/user/setup_spool` must perform the following setup idempotently (it must succeed with exit code 0 and result in the exact same target state whether run once or multiple times consecutively):

1. **Directory Structure & Permissions**: 
   Create the base directory `/home/user/mail_spool` and its subdirectories:
   `/home/user/mail_spool/inbox`
   `/home/user/mail_spool/outbox`
   `/home/user/mail_spool/archive`
   All of these directories must have their permissions explicitly set to `0750` (user: rwx, group: rx, others: none).

2. **Timezone Link Management**:
   Create a symbolic link at `/home/user/mail_spool/tz_local` that strictly points to `/usr/share/zoneinfo/Europe/Paris`. 
   *Note: Because this is an idempotent tool, if the symlink already exists, the program must handle it gracefully without crashing, ensuring it ultimately points to the correct location.*

3. **Locale & Mailing List Configuration**:
   Create a text file at `/home/user/mail_spool/mailer.conf` with permissions `0640` (user: rw, group: r, others: none). 
   The file must contain exactly these two lines (with a newline at the end of each):
   `MAILING_LIST_TZ=Europe/Paris`
   `LC_TIME=fr_FR.UTF-8`

Execute your compiled program at least once before completing the task so the target directories and files are present on the system.