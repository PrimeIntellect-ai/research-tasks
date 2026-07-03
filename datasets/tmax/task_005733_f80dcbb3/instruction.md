You are acting as an infrastructure engineer tasked with automating the provisioning of a custom backup utility. Because you do not have root access, you will be configuring user-space equivalents and automation scripts.

Please complete the following provisioning phases:

**Phase 1: Environment Variables**
Create a profile file at `/home/user/.backup_profile` that exports the following environment variables:
- `BACKUP_SOURCE=/home/user/data`
- `BACKUP_DEST=/home/user/backups/data`
- `BACKUP_RETENTION_DAYS=14`

**Phase 2: Mount Configuration**
We use a user-space mounting wrapper that reads a custom fstab-like file. Create a file at `/home/user/custom_fstab` with exactly one line representing a bind mount from the source to the destination. It must follow the standard fstab format (6 fields separated by spaces or tabs):
`<file system> <mount point> <type> <options> <dump> <pass>`
Map `/home/user/data` to `/home/user/backups/data` with type `none`, options `bind`, dump `0`, and pass `0`.

**Phase 3: Interactive Automation**
There is a pre-existing interactive configuration utility at `/home/user/bin/init_backup.py`. When run, it prompts exactly as follows:
1. `Source directory: `
2. `Destination directory: `
3. `Retention days: `
4. `Proceed with setup? (y/n): `

Write a Python script at `/home/user/auto_provision.py` that uses the `pexpect` library to automate running `/home/user/bin/init_backup.py`. Your script should:
- Start the `init_backup.py` process.
- Answer the prompts using the exact paths and retention days specified in Phase 1.
- Answer `y` to the final prompt.
- Wait for the process to exit.
After writing your script, execute it so that the backup utility is fully configured.

**Phase 4: Scheduled Task**
Configure the current user's crontab to run the backup job automatically. Add a cron entry that executes `/home/user/bin/run_backup.sh` every day at exactly 2:30 AM.

Ensure all files are created exactly at the specified paths. Do not assume any pre-existing crontab entries.