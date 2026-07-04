You are tasked with building an automated configuration manager script in Python to process server backups, track approved changes, and update configuration files.

Workspace: `/home/user/config_manager`

In the `/home/user/config_manager/backups` directory, there are several `.tar.gz` backup archives containing server configurations and logs. Some of these archives may have been corrupted during transfer. 

Additionally, there is a global configuration file at `/home/user/config_manager/rules.ini` that dictates network changes.

You must write a Python script (e.g., `manager.py`) and execute it to perform the following operations:

1. **Dependency Management & Concurrency:** 
   Your script must be able to process the valid server archives concurrently (using `multiprocessing` or `concurrent.futures`). Because multiple processes will be writing to a shared log file, you MUST use file locking (e.g., using `fcntl` or the `filelock` package which you can install via pip) to prevent race conditions when writing to the output file.

2. **Configuration Interpretation:**
   Parse the `/home/user/config_manager/rules.ini` file to find the `legacy_ip` and `new_ip` under the `[Network]` section.

3. **Archive Integrity & Extraction:**
   Iterate through all `.tar.gz` files in `/home/user/config_manager/backups`. Verify the structural integrity of each archive before extraction. 
   - If an archive is corrupted, safely catch the error and record exactly this line to the shared log file: `Corrupted: <filename>`
   - If valid, extract it into `/home/user/config_manager/extracted/<archive_name_without_tar_gz>/`.

4. **Multi-line Log Record Parsing:**
   Inside each valid extracted directory, there is a `changelog.txt` file containing multi-line deployment records. 
   A record looks like this:
   ```
   [Deployment: 2023-10-05]
   CommitID: a1b2c3d
   Status: REJECTED
   Changes:
     - Updated firewall rules
   ```
   You must parse this file to find the `CommitID` of the **most recent** (closest to the bottom of the file) record that has `Status: APPROVED`. 

5. **Large-scale Text Editing:**
   Inside each valid extracted directory, there is a large configuration file named `app.conf`. You must perform a macro replacement: replace every occurrence of the `legacy_ip` (read from `rules.ini`) with the `new_ip`. Overwrite the `app.conf` file with these changes.

6. **Reporting (File Locking required):**
   For every valid archive processed, safely append (using your file locking mechanism) the following line to `/home/user/config_manager/results.log`:
   `Processed: <extracted_folder_name> - ApprovedCommit: <commit_id>`

**Final state verification requirements:**
- All dependencies must be cleanly installed.
- `/home/user/config_manager/results.log` must exist, contain the `Corrupted:` lines for invalid archives, and the `Processed:` lines for valid ones (order does not matter).
- All `app.conf` files in the extracted directories must have the IPs successfully updated.