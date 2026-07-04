You are acting as a backup administrator trying to fix a broken archival process. A previous automated backup script attempted to archive the `/home/user/data` directory but crashed because it aggressively followed symlinks, resulting in infinite loops. 

The crashed script left behind a multi-line log file at `/home/user/backup.log`. You need to write a Bash script at `/home/user/safe_backup.sh` that performs the following steps:

1. **Parse the Log:**
   Read `/home/user/backup.log`. The log consists of multi-line records in the following format:
   ```text
   --BEGIN--
   Target: <absolute_path>
   Status: <OK|ERROR>
   Details: <Error message or success note>
   --END--
   ```
   Using tools like `awk`, `sed`, or `grep`, extract the exact `Target` paths for all records where the `Details` line explicitly contains the phrase `Symlink loop`. 
   Save these extracted paths (one per line) into a file named `/home/user/exclude.txt`.

2. **Create the Archive:**
   Use the `tar` command to create a compressed gzip archive of the `/home/user/data` directory. 
   - The archive must be saved to `/home/user/safe_backup.tar.gz`.
   - You MUST exclude all the paths listed in `/home/user/exclude.txt` from the archive. Use `tar`'s built-in exclusion functionality (e.g., `--exclude-from`).
   - Archive the directory using its absolute path (`/home/user/data`).

Make sure your script `/home/user/safe_backup.sh` is executable (`chmod +x`) and runs without errors. Once you have created and executed the script, verifying that `safe_backup.tar.gz` and `exclude.txt` are created correctly, you are done.