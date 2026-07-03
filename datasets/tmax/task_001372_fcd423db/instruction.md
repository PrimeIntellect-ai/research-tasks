You are tasked with creating a Python-based configuration deployment script that safely moves configuration files from a staging area to a live production directory. 

You need to write a script at `/home/user/deploy_configs.py` that performs the following operations:

1. **Configuration Interpretation & Filtering**: Iterate over all `.conf` files in `/home/user/staging/`. Each file is in a simple `key=value` format (one per line). Read the file and check if it contains the exact line `DEPLOY=true`. If it does not, skip the file.
2. **Hard Link Backup**: If a file scheduled for deployment already exists in `/home/user/live/` with the same name, you must back up the existing live file *before* deploying the new one. Back it up by creating a hard link in `/home/user/backup/` named `<filename>.bak` (e.g., `app.conf.bak`). Do not copy the file; it must be a hard link. If a backup already exists, remove it before creating the new hard link.
3. **Atomic Writes**: Deploy the new configuration from staging to `/home/user/live/` atomically. To do this, you must write or copy the staging file contents to a temporary file in the live directory named `.<filename>.tmp` (e.g., `/home/user/live/.app.conf.tmp`), and then atomically rename/replace it to `/home/user/live/<filename>`.
4. **Streaming/Appending Log**: For every file successfully deployed, append a line to `/home/user/deploy.log` in the exact format: `Successfully deployed <filename>`.

Once you have written the script, execute it so the deployment takes place.

**Initial State:**
- Staging directory: `/home/user/staging/`
- Live directory: `/home/user/live/`
- Backup directory: `/home/user/backup/`
- Log file: `/home/user/deploy.log`

Please ensure your script is robust and strict about the paths and naming conventions provided.