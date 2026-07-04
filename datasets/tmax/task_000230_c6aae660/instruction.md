You are an operations engineer tasked with setting up a local "manifest manager" (similar to a simple Kubernetes operator) that processes configuration files. We have an existing system that is failing because of missing dependency sequencing and directory structures.

Your objective is to complete the following phases:

**Phase 1: Directory Structure Management**
Create the following directories:
- `/home/user/manifests/raw`
- `/home/user/manifests/active`
- `/home/user/manifests/versions`
- `/home/user/logs`
- `/home/user/.config/validator`

Assume that two files, `app1.json` and `app2.json`, will be placed in `/home/user/manifests/raw/` by an external process. 

**Phase 2: Idempotent Configuration Scripting**
Write a Python script at `/home/user/operator.py` that acts as the manifest manager. 
When executed, this script must:
1. Scan `/home/user/manifests/raw/` for any `.json` files.
2. For each file, calculate the MD5 hash of its contents.
3. Copy the file to `/home/user/manifests/versions/<filename_without_ext>_<md5hash>.json`.
4. Create or forcefully update a symbolic link at `/home/user/manifests/active/<filename>` that points to the newly created versioned file.
5. Ensure the script is idempotent (running it multiple times should not error out or create duplicate/dangling symlinks).

**Phase 3: Fixing the Missing Dependency (The Anchor)**
There is an existing script at `/home/user/validator.py` which validates the active manifests. However, it currently crashes because it requires a specific initialization state that hasn't been met (simulating a missing `After=` dependency in systemd). Specifically, `validator.py` crashes if the file `/home/user/.config/validator/init.flag` does not exist with the exact text `READY` inside it.

Write a bash script at `/home/user/run_system.sh` that safely sequences the startup:
1. Writes the word `READY` (followed by a newline) into `/home/user/.config/validator/init.flag`.
2. Executes `/home/user/operator.py`.
3. Executes `python3 /home/user/validator.py` and redirects its standard output to `/home/user/logs/validation_report.txt`.

Make sure `/home/user/run_system.sh` is executable.

**Phase 4: Scheduled Task Configuration**
Install a user-level crontab that executes `/home/user/run_system.sh` every minute.

To finish the task, ensure the environment is fully set up, the script `/home/user/run_system.sh` has been executed at least once manually so that `/home/user/logs/validation_report.txt` is populated, and the cron job is installed.