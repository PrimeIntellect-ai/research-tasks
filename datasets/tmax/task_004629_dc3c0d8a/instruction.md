You are a deployment engineer rolling out a configuration update for a legacy application across multiple user accounts. Because of strict environment constraints, you need to write a C program to automate this rollout. 

A simulated user database is located at `/home/user/mock_passwd` (formatted identically to `/etc/passwd`). 
The application configuration for each user is managed via a symlink named `app_config` in their respective home directories (as specified in the mock passwd file). Currently, these symlinks point to the old release: `/home/user/releases/v1/config.ini`.

Your task is to write and execute a C program at `/home/user/rollout.c` that does the following:
1. Reads `/home/user/mock_passwd`.
2. Identifies all users who belong to the primary Group ID (GID) `1001`.
3. For each identified user:
   a. Updates the `app_config` symlink in their simulated home directory to point to the new release: `/home/user/releases/v2/config.ini`.
   b. Generates a log rotation configuration block for the user's application logs and appends it to `/home/user/logrotate_updates.conf`. 

The log rotation block for each updated user must exactly match this format (where `<username>` and `<homedir>` are replaced with the user's actual username and home directory from the mock passwd file):
```
<homedir>/logs/*.log {
    daily
    rotate 7
    compress
}
```

Ensure your C program compiles with standard GCC (`gcc /home/user/rollout.c -o /home/user/rollout`) and executes successfully. Leave the generated logrotate file and the modified symlinks in place for verification.