You are a backup operator testing a restore of an email server configuration. The remote backup server has been configured to silently reject SSH key-based logins, forcing an interactive password prompt. 

You need to automate the download of the backup archive, extract it, and write a C program to reconstruct the mail server's directory structure and apply the correct Access Control Lists (ACLs).

Perform the following steps:
1. An executable named `/home/user/fetch_backup` exists. When run, it simulates the SSH connection and will prompt you interactively with exactly: `Password for backup server: `
2. Write an Expect script at `/home/user/fetch.exp` that executes `/home/user/fetch_backup` and automatically provides the password `SecureRest0re!`. 
3. Run your Expect script. If successful, it will drop a tarball named `/home/user/mail_data.tar` in your home directory.
4. Extract `/home/user/mail_data.tar` into `/home/user/mail_data/`. It contains `postfix/main.cf` and `dovecot/dovecot.conf`.
5. Write a C program at `/home/user/reconstruct.c` and compile it to `/home/user/reconstruct`. The C program must:
   - Use the POSIX `mkdir()` function to create the directory `/home/user/live_mail` (with `0755` permissions).
   - Use the POSIX `symlink()` function to create a symlink at `/home/user/live_mail/postfix` that points to `/home/user/mail_data/postfix`.
   - Use the POSIX `symlink()` function to create a symlink at `/home/user/live_mail/dovecot` that points to `/home/user/mail_data/dovecot`.
   - Execute shell commands (e.g., via `system()`) to set ACLs so that the unprivileged user `nobody` has exact read and execute permissions (`r-x`) on the `/home/user/mail_data/postfix` directory, and exact read permissions (`r--`) on `/home/user/mail_data/postfix/main.cf`.
6. Run your compiled `/home/user/reconstruct` program to finalize the system state.

Constraints:
- Do not use root (`sudo`). All files should be owned by `user`.
- Ensure you install or compile correctly in the `/home/user` directory.