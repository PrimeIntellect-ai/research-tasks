You are tasked with fixing a broken configuration backup process. A previous backup tool failed to archive certain application configurations because it got stuck in infinite symlink loops. 

You need to write and execute a Python script at `/home/user/archive_configs.py` that performs the following steps:

1. **Parse the Backup Log:**
   Read the multi-line log file located at `/home/user/backup.log`. The log entries are separated by a line containing exactly `--`. 
   Identify all `TARGET` directories from log entries where the `STATUS` is `FAILED` and the `REASON` is `SYMLINK_LOOP`.

2. **Securely Archive the Configurations:**
   For each identified target directory, create a compressed tarball (`.tar.gz`) in the `/home/user/archives/` directory. The archive name should be `<dirname>.tar.gz` (e.g., if the target is `/home/user/configs/app_beta`, the archive should be `/home/user/archives/app_beta.tar.gz`).
   
   When archiving:
   - Traverse the target directory.
   - You must dereference (follow) symlinks and archive the actual file contents, not the symlink itself.
   - **Symlink Management:** Detect symlinks that form infinite loops. If a symlink forms a loop, **skip it entirely** (do not add it to the archive).
   - Log the absolute paths of all skipped symlink files to `/home/user/skipped_links.txt`, one path per line, sorted alphabetically.
   - **File Locking:** The configuration files might be actively written to by other services. Before reading any regular file to add it to the archive, your script must open the file and acquire a shared lock using `fcntl.flock(fd, fcntl.LOCK_SH)`. Release the lock after reading.

3. **Archive Structure:**
   The files inside the tarball should not include the absolute path structure leading up to the target directory. For example, `/home/user/configs/app_beta/config.ini` should appear as `config.ini` (or `./config.ini`) at the root of `app_beta.tar.gz`.

Create the `/home/user/archives/` directory if it does not exist, write your Python script, and run it to produce the expected archives and the `skipped_links.txt` file.