You are an infrastructure engineer automating the provisioning of a lightweight, custom mail server health monitor. We have a localized mail spool at `/home/user/mail_spool` that occasionally backs up with too many un-dispatched messages.

Your task is to write a C program that acts as a health check and automated backup trigger. 

Create a C source file at `/home/user/mail_monitor.c` that does the following when executed:
1. Opens and reads the directory `/home/user/mail_spool`.
2. Counts the number of regular files (excluding `.` and `..` or directories) inside this directory.
3. If the file count is strictly greater than 5, the C program must execute a shell command (using `system()`) to create a compressed backup of the directory. The backup must be created at `/home/user/mail_backup.tar.gz` and should contain the `mail_spool` directory (use `tar -czf /home/user/mail_backup.tar.gz -C /home/user mail_spool`).
4. Finally, the C program must open `/home/user/health_status.log` and write a single line detailing the health check result. If the backup was triggered, write:
   `STATUS: BACKUP_TRIGGERED, EMAIL_COUNT: X`
   (Where `X` is the integer count of regular files found).
   If the count was 5 or fewer, it should write:
   `STATUS: HEALTHY, EMAIL_COUNT: X`

After writing the C code, compile it using GCC into an executable named `/home/user/mail_monitor`, and then run the executable once so it performs its checks on the current system state.

Requirements:
- Ensure the output log format exactly matches the specification.
- Use standard POSIX C libraries (`<stdio.h>`, `<stdlib.h>`, `<dirent.h>`, etc.).
- Do not hardcode the expected file count; your program must count the files dynamically.