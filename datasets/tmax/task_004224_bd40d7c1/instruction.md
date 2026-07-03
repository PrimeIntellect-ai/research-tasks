You are an infrastructure engineer automating a local provisioning and backup system. 

You need to write a C program that acts as a backup provisioning tool. The tool will check a simulated storage quota for various system users and, if they are within their allowed storage limits, back up their data.

Here is the setup of the system you are working with:
- There is a text file at `/home/user/quota_data.txt` containing user quota information. Each line is formatted as `username:used_bytes:quota_bytes`.
- There is a directory at `/home/user/user_data/` containing subdirectories for each user (e.g., `/home/user/user_data/alice/`, `/home/user/user_data/bob/`).
- There is an empty directory at `/home/user/backups/` where backups should be stored.

Your task:
1. Write a C program saved at `/home/user/provision_backup.c` and compile it to an executable named `/home/user/provision_backup`.
2. The program must read `/home/user/quota_data.txt`.
3. For each user in the file:
   - Compare `used_bytes` to `quota_bytes` (both as integers).
   - If `used_bytes` is LESS THAN OR EQUAL TO `quota_bytes`, the program must create a compressed tarball (`.tar.gz`) of the user's data directory. The command executed by your C program (e.g., via `system()`) should be equivalent to: `tar -czf /home/user/backups/<username>_backup.tar.gz -C /home/user/user_data <username>`
   - If `used_bytes` is GREATER THAN `quota_bytes`, do not back up their directory.
4. The program must write a log of its decisions to `/home/user/provision.log`. Append a line for each user in the exact format:
   - If backed up: `BACKUP_SUCCESS: <username>`
   - If over quota: `QUOTA_EXCEEDED: <username>`

Run your compiled executable so that the backups and log file are generated.