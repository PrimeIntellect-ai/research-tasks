You are tasked with setting up a Git-based automated backup restoration testing pipeline. As a backup operator, you need to ensure that whenever a backup manifest is committed and pushed to our vault, the system automatically stages a simulated restore, manages directory symlinks, and registers the virtual mount points in a mock fstab configuration.

All your work must take place within `/home/user/`. You do not have root access.

Please complete the following steps:

1. **Git Vault Setup:**
   - Create a bare Git repository at `/home/user/backup_vault.git`.

2. **Automated Restore Hook (Python):**
   - Create a `post-receive` Git hook in Python 3 at `/home/user/backup_vault.git/hooks/post-receive`.
   - Make sure the hook is executable.
   - The hook must read from standard input to get the old revision, new revision, and branch reference (standard Git `post-receive` behavior).
   - For every push, the hook must:
     a) Extract the tree of the pushed commit into a new directory: `/home/user/restores/<commit_hash>`.
     b) Update (or create) a symbolic link at `/home/user/restores/latest` pointing to this newly created directory.
     c) Read `restore_manifest.json` from the extracted files.
     d) Append a single line to `/home/user/mock_fstab` based on the manifest. The format must be: `<archive_name> <mount_target> auto defaults 0 0`. (Create `mock_fstab` if it doesn't exist).

3. **Interactive Verification Script (Python):**
   - Create a Python script at `/home/user/verify_restore.py`.
   - This script must prompt the user interactively with exactly: `Verify latest restore? [y/N]: `
   - If the user inputs `y` or `Y`, the script must read `/home/user/restores/latest/restore_manifest.json`.
   - It should then format a message: `SUCCESS: Restore registered for <archive_name> at <mount_target>` and append this exact line to `/home/user/restore_test.log`.
   - If the user inputs anything else, it should exit without writing to the log.

4. **Trigger the Pipeline:**
   - Clone the bare repository locally to `/home/user/workspace`.
   - In the workspace, create a file named `restore_manifest.json` with the following exact JSON content:
     ```json
     {
       "archive": "db_backup_v9.tar.gz",
       "mount_target": "/home/user/mnt/recovery_db"
     }
     ```
   - Commit this file with the message "Initial backup manifest" and push it to the `master` branch of the `backup_vault.git` remote.
   - Finally, run your interactive script and simulate a "yes" response to write the verification log. You can do this by running: `echo "y" | python3 /home/user/verify_restore.py`.