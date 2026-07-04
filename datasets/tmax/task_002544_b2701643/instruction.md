You are a site administrator managing user accounts. You have a Go-based backup system that runs as a simulated cron job, but it is currently writing backups to the wrong location due to working directory differences when executed in the cron environment. 

Your tasks are:

1. **Fix the Backup Script**: 
   There is a Go program at `/home/user/backup.go` that archives user data. When executed via the simulated cron script `/home/user/cron_run.sh`, the backup file (`users.tar.gz`) is created in the wrong directory (`/tmp`) because the Go code uses a relative path.
   Modify `/home/user/backup.go` so that the tar command explicitly writes the output file to the absolute path: `/home/user/backups/users.tar.gz`.
   After fixing it, execute `/home/user/cron_run.sh` to generate the backup correctly.

2. **Automate the Restore Test (CI/CD primitive)**:
   There is an interactive script at `/home/user/restore.sh` that prompts for the backup file path and extracts it. 
   Write an Expect script at `/home/user/test_restore.exp` that automates this. The Expect script must:
   - Spawn `/home/user/restore.sh`
   - Wait for the exact prompt: `Enter backup file path: `
   - Send the absolute path `/home/user/backups/users.tar.gz` followed by a newline.
   - Wait for the output: `Restore complete`
   Run your Expect script to perform the restoration. It should extract the files into `/home/user/restored_data/`.

3. **Prepare Storage Configuration**:
   Create a file at `/home/user/fstab_entry.txt` containing exactly one line representing an fstab entry to mount a backup drive. Use the following parameters:
   - UUID: `1234-5678-ABCD`
   - Mount point: `/home/user/backups`
   - Filesystem type: `ext4`
   - Options: `defaults`
   - Dump: `0`
   - Pass: `2`

Ensure all specified directories exist and all output files are exactly where requested.