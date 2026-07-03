You are tasked with helping a developer organize a messy directory of project log files based on embedded metadata and a configuration file. 

You need to write a Python script at `/home/user/organizer.py` that processes the log files and organizes them into a new directory structure. 

Here are the requirements:

1. **Directories & Config:**
   - Source directory: `/home/user/project_logs/` (contains several `.log` files).
   - Target directory: `/home/user/organized_logs/` (you will need to create this and subdirectories).
   - Config file: `/home/user/organizer_config.json`. This file contains a "mapping" dictionary that maps "module" names to target subdirectory names.

2. **Log File Format:**
   - The `.log` files contain multi-line plain text log entries.
   - Somewhere in each file, there is a multi-line embedded JSON payload enclosed exactly between the lines `<<<JSON_START>>>` and `<<<JSON_END>>>`.
   - The JSON object contains three keys: `"module"`, `"severity"`, and `"id"`.

3. **Processing Logic:**
   - Iterate through every `.log` file in `/home/user/project_logs/`.
   - **File Locking:** Before reading and moving a file, you MUST acquire an exclusive lock on the file using `fcntl.flock(fd, fcntl.LOCK_EX)`. This is required because background worker processes might occasionally check these files.
   - Extract and parse the embedded JSON payload.
   - Look up the `"module"` in `/home/user/organizer_config.json` to find the correct subdirectory name.
   - Move and rename the file to `/home/user/organized_logs/<subdirectory_name>/<severity>_<id>.log`.
   - If a target subdirectory does not exist, your script must create it.
   - Remove the lock only after the file has been successfully moved (or if an error occurs).

Write and execute the `/home/user/organizer.py` script so that all files in `/home/user/project_logs/` are successfully organized into `/home/user/organized_logs/`.