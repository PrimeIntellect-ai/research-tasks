You are a Linux systems engineer responsible for hardening configuration files and writing custom compliance checks. 

Your objective is to secure a specific configuration file and write a C utility that programmatically verifies its filesystem permissions.

Perform the following steps:

1. **Configuration Creation**: 
   - Create a directory at `/home/user/config_vault`.
   - Inside it, create a file named `app_config.json` containing exactly the string `{"status":"locked"}` without any trailing newline.

2. **Permission Hardening**:
   - Secure the directory `/home/user/config_vault` so that only the owner can read, write, and execute it (exact octal mode `0700`).
   - Secure the file `/home/user/config_vault/app_config.json` so that it is strictly read-only for the owner, with no permissions for group or others (exact octal mode `0400`).

3. **C-based Compliance Checker**:
   - Write a C program at `/home/user/check_perms.c`.
   - This program must use the `stat` system call to verify the permissions of BOTH `/home/user/config_vault` and `/home/user/config_vault/app_config.json`.
   - If `/home/user/config_vault` is exactly `0700` AND `app_config.json` is exactly `0400`, the program should print exactly `SECURE` to standard output (followed by a newline).
   - If either file/directory does not exist, or if the permissions do not match the exact strict requirements above, the program should print exactly `INSECURE` to standard output (followed by a newline).
   - Compile this program to an executable located at `/home/user/check_perms`.

4. **Wrapper Script**:
   - Create an executable bash script at `/home/user/verify.sh`.
   - The script must strictly set the environment variables `TZ=UTC` and `LC_ALL=C`.
   - It must then execute `/home/user/check_perms` and redirect its standard output to `/home/user/security_status.txt`.

5. **Execution**:
   - Run `/home/user/verify.sh` so that `/home/user/security_status.txt` is generated.