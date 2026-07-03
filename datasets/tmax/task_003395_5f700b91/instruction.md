You are a network engineer tasked with troubleshooting a severe connectivity issue. A custom SSH-like connectivity manager has been silently rejecting key-based logins for legitimate administrators. The vendor has provided a diagnostic oracle binary, but the original configuration files were lost during a botched migration.

Your objective is to write a Python script `/home/user/rebuild_config.py` that reconstructs the correct configuration bundle from raw system logs, sets up the expected environment formats, and verifies the fix against the vendor's oracle.

Here is the context:
1. **The Diagnostic Oracle:**
   There is a stripped, compiled binary located at `/app/net_oracle`. This binary simulates the authentication daemon's behavior. It takes a single argument: the path to a configuration bundle directory. 
   It evaluates the bundle and outputs a JSON response with an `accuracy` score (a float between 0.0 and 1.0) indicating how well the configuration resolves the silent rejection bugs.

2. **The Raw Logs:**
   You have a log file at `/home/user/connection_logs.txt`. 
   Each line has the format:
   `[TIMESTAMP] | IP:PORT | USER | ACTION | STATUS | KEY_DATA`
   Due to the bug, legitimate keys for the user `netadmin` during the `KEY_EXCHANGE` action were marked with the status `REJECTED_SILENTLY`. You need to use Python (leveraging text processing pipelines or regex) to parse this log file and extract the `KEY_DATA` only for these specific falsely-rejected attempts.

3. **The Configuration Bundle Requirements:**
   Your Python script must create a directory at `/home/user/net_bundle/` and populate it with the following files to simulate the system environment the daemon expects:
   
   - `authorized_keys`: This file must contain all the unique, valid `KEY_DATA` strings extracted from the logs (one per line).
   - `fstab_snippet`: The daemon requires the keys directory to be mounted in memory for security. Write a valid `fstab` line that would mount a `tmpfs` filesystem to the path `/home/user/keys_mnt`. The mount must include the `noexec`, `nosuid`, and `nodev` options.
   - `group_snippet`: The daemon checks user group memberships via a simulated group file. Create a file mimicking the standard `/etc/group` format. It must define a group named `ssh_mgrs` (with any GID, e.g., 2000) and include the user `netadmin` as a member.

4. **Integration and Execution:**
   Your Python script `/home/user/rebuild_config.py` should:
   - Parse `/home/user/connection_logs.txt`.
   - Generate the `/home/user/net_bundle/` directory and the three required files.
   - Run the `/app/net_oracle /home/user/net_bundle/` binary via Python's subprocess module.
   - Print the oracle's JSON output to the console.

Write the Python script to be robust, handling file creation and ensuring no duplicate keys are written. 
You must achieve an accuracy score of at least 0.95 from the oracle to successfully resolve the issue.