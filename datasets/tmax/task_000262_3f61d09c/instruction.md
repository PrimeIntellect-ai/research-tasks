You are acting as a site administrator for a shared application environment. The system manages user accounts and monitors their storage quotas. Recently, the monitoring service has been failing because of a dependency issue, and the account provisioning process requires manual interaction. 

You need to complete the following tasks to fully automate and fix the monitoring pipeline:

1. **Fix the Service Dependency**:
   There is a systemd service file located at `/home/user/app/account-monitor.service`. It currently fails during startup because it attempts to read data before the storage is initialized. 
   Edit `/home/user/app/account-monitor.service` and add `After=storage-init.service` to the `[Unit]` section. Leave the rest of the file unmodified.

2. **Automate Provisioning using Expect**:
   There is a bash script at `/home/user/app/provision.sh` that requires interactive input. It prompts for:
   - `Enter Admin PIN: `
   - `Action (1=Init, 2=Clear): `
   
   Write an `expect` script at `/home/user/app/auto_provision.exp` that executes `/home/user/app/provision.sh`. Your expect script must automatically provide the PIN `8821` and the Action `1`. The expect script must exit cleanly (return 0) after completion. Make sure to make it executable.

3. **Storage Monitoring Script**:
   Write a bash script at `/home/user/app/check_quota.sh` that checks the total disk space used by the directory `/home/user/app/users/`. 
   - Use `du -sb /home/user/app/users/` to calculate the total size in bytes.
   - If the size is strictly greater than `10000` bytes, append the exact string `QUOTA_EXCEEDED` (followed by a newline) to `/home/user/app/quota.log`.
   - If the size is `10000` bytes or less, append the exact string `OK` (followed by a newline) to `/home/user/app/quota.log`.
   - Ensure `/home/user/app/check_quota.sh` is executable.

4. **Scheduled Task**:
   Use `crontab` to schedule the script `/home/user/app/check_quota.sh` to run every 5 minutes. The cron schedule expression should be exactly `*/5 * * * *`.

Ensure all file paths and exact string matches are respected. You may create `/home/user/app/users/` if it does not already exist, to test your bash script.