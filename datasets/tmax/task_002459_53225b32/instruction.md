You are an infrastructure engineer automating the provisioning of a local backup system for a legacy application. A recent security update has caused an internal SSH configuration to silently reject key-based logins, forcing you to use an interactive legacy shell script for backups until the issue is resolved. 

Your task is to prepare the backup volume, update a mock system configuration, and automate the interactive backup script using Python.

Perform the following tasks:

1. **Storage Preparation**:
   Create a 20MB empty file at `/home/user/backup.img`. Format this file as an `ext4` filesystem. Do not attempt to mount it (as you do not have root privileges), but ensure the filesystem is properly initialized.

2. **fstab Configuration**:
   There is a mock fstab file located at `/home/user/system_fstab`. Append a new entry to this file to configure the mounting of your new backup image. The entry must specify:
   - File system: `/home/user/backup.img`
   - Mount point: `/home/user/mnt_backup`
   - Type: `ext4`
   - Options: `loop,defaults`
   - Dump: `0`
   - Pass: `2`
   Ensure the fields are separated by spaces or tabs.

3. **Expect Scripting (Python)**:
   There is an interactive backup tool located at `/home/user/legacy_backup.sh`. Because key-based authentication is currently broken, it requires interactive input.
   Write a Python script at `/home/user/run_provision.py` that uses the `pexpect` module to automate the execution of `/home/user/legacy_backup.sh`.
   
   The interactive script will output the following prompts (wait for these exact strings):
   - `Password:` -> You must send `SecretPass99`
   - `Source path:` -> You must send `/home/user/app_data`
   - `Destination tarball:` -> You must send `/home/user/app_data_backup.tar.gz`

   Execute your Python script so that it successfully drives the bash script and generates the tarball.

4. **Verification Log**:
   Create a log file at `/home/user/provision_summary.log` containing exactly three lines in this format:
   ```
   FSTAB_CONFIGURED=true
   BACKUP_ARCHIVE_CREATED=[true/false]
   BACKUP_IMG_SIZE=[size in bytes]
   ```
   Replace `[true/false]` with `true` if `/home/user/app_data_backup.tar.gz` was created, and `[size in bytes]` with the exact file size of `/home/user/backup.img` in bytes.