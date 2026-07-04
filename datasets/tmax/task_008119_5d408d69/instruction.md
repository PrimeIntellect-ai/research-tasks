You are tasked with building a Bash-based configuration manager that tracks, parses, and distributes Write-Ahead Log (WAL) changes to various system components. 

You need to create a directory structure, write a daemon script to watch for incoming changes, parse a custom WAL format, and split the updates into separate configuration files.

**Requirements:**

1. **Directory Setup:**
   Create the following directories:
   - `/home/user/wal_incoming`
   - `/home/user/wal_processed`
   - `/home/user/config_active`

2. **The Watcher Daemon (`/home/user/config_watcher.sh`):**
   Write a Bash script at `/home/user/config_watcher.sh` that acts as a continuous file watcher. Since you do not have root access to install extra packages like `inotify-tools`, implement a polling loop (e.g., checking every 1 second) to detect new files ending in `.wal` inside `/home/user/wal_incoming/`.
   - The script must be executable.
   - Run this script in the background (e.g., using `nohup` or `&`) so it continues running after your job is done.

3. **Parsing and Splitting the WAL Format:**
   When a `.wal` file is detected, parse it line by line. 
   The custom WAL format consists of lines structured exactly like this:
   `TXN:[TransactionID]|SYS:[SubsystemName]|CMD:[ConfigurationCommand]`
   
   For each valid line:
   - Extract the `SubsystemName` and the `ConfigurationCommand`.
   - Append the `ConfigurationCommand` (along with a trailing newline) to a file named `/home/user/config_active/[SubsystemName].conf`. Create the file if it does not exist.
   - Ignore lines that do not strictly match this format (e.g., empty lines or comments starting with `#`).

4. **Lifecycle Management:**
   After a `.wal` file has been completely parsed and its contents distributed, move the file to `/home/user/wal_processed/`.

5. **Validation:**
   Start your watcher script in the background. To test it yourself, you may create a mock `.wal` file in the incoming directory and verify it is processed. 
   Leave the background process running when you finish the task. The automated verification system will drop a secret `.wal` file into `/home/user/wal_incoming/` and evaluate whether the correct `.conf` files are generated and populated within 5 seconds.