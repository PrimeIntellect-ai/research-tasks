You are a cloud architect migrating services to a new infrastructure. Part of this migration involves replacing a legacy binary data processor with a maintainable Python script, alongside setting up proper automation, logging, and version control hooks.

Your tasks are:

1. **Reverse Engineer the Legacy Service:**
   There is a stripped binary located at `/app/legacy_processor`. It reads arbitrary text from standard input (`stdin`) and writes processed text to standard output (`stdout`). 
   By experimenting with this binary, deduce its text transformation algorithm. 
   Write a Python script at `/home/user/new_processor.py` that exactly replicates the behavior of `/app/legacy_processor`. Your script must read from standard input, process the text, and print the result to standard output. It must produce bit-exact equivalent output for any given input.

2. **Task Automation & Connectivity Diagnostics:**
   Write a bash script at `/home/user/check_and_run.sh`. When executed, this script should:
   - Check if a local service is listening on TCP port `8080`.
   - If port 8080 is reachable, read all `.log` files in `/home/user/incoming_logs/`, process them using your `new_processor.py`, and append the output to `/home/user/processed/master.log`.
   - If port 8080 is not reachable, append the exact string `ERROR: Port 8080 unreachable` to `/home/user/processed/error.log`.

3. **Log Configuration and Rotation:**
   Create a logrotate configuration file at `/home/user/logrotate.conf` to manage the logs in `/home/user/processed/`. The configuration must specify:
   - Daily rotation.
   - Keep 7 days of backlogs.
   - Compress old log files.
   - Delay compression of the most recent rotated file.
   - Missing log files should not cause an error.

4. **Git Setup and Hook Configuration:**
   Initialize a Git repository in `/home/user/migration_repo`. 
   Configure a `pre-commit` hook in this repository that scans all staged Python (`.py`) files. If any staged Python file contains the string `DEBUG_MODE=True`, the commit must be rejected (exit code 1) and the hook should print `No debug code allowed!`. Otherwise, the commit should proceed.

Ensure all scripts are executable and have the correct file paths.