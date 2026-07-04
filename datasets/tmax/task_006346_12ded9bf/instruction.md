You are acting as a backup operator who needs to test the restore process of a server's critical configuration files. We have a backup archive of email server and virtualization configuration files located at `/home/user/backup_data.tar.gz`.

Your objective is to write an automated, idempotent validation pipeline that extracts this backup and verifies its contents using a custom C program.

Please perform the following steps:

1. **Write the C Validation Tool:**
   Write a C program at `/home/user/verify_restore.c` and compile it to `/home/user/verify_restore`.
   The program must:
   - Take exactly one command-line argument: the path to the extracted directory.
   - Count the total number of *regular files* located directly within that directory (do not recurse into subdirectories).
   - Read the file named `mail_config.conf` located inside that directory.
   - Parse the numeric value associated with the `SMTP_PORT` key in that file (the file contains lines like `KEY=VALUE`).
   - Print a single line to standard output in exactly this format:
     `RESTORE_CHECK: SUCCESS, FILES: <file_count>, PORT: <parsed_port>`

2. **Write the Validation Script:**
   Write a Bash script at `/home/user/run_validation.sh` that automates the restore test safely and idempotently. The script must:
   - Ensure the directory `/home/user/restore_test` exists. If it already exists, safely empty it so the test starts fresh.
   - Extract the contents of `/home/user/backup_data.tar.gz` directly into `/home/user/restore_test`.
   - Execute the compiled C tool `/home/user/verify_restore`, passing `/home/user/restore_test` as the argument.
   - Redirect the standard output of the C tool to `/home/user/restore_log.txt`.

Make sure `/home/user/run_validation.sh` is executable and run it to produce the final log file. 

The automated test will verify the contents of `/home/user/restore_log.txt` and inspect your C code and shell script. Do not hardcode the expected output in the C file; it must calculate the count and parse the port dynamically.