You are tasked with building a robust configuration tracking daemon in Python that monitors legacy configuration files, handles encoding conversions on the fly, uses memory-mapped I/O for efficient reading, and creates differential backups in a continuous archive.

Here is the scenario:
You have a legacy system that writes configuration files (`*.ini`) to `/home/user/legacy_configs`. These files are historically encoded in `ISO-8859-1`. We need a tracking script that detects changes to these files, converts them to `UTF-8`, computes the difference from the last known state, and archives the diffs.

Please perform the following steps:

1. Create a Python script at `/home/user/config_tracker.py` that does the following:
   - Takes two command-line arguments: the directory to watch, and the path to the backup archive (a `.tar` file). Example: `python3 /home/user/config_tracker.py /home/user/legacy_configs /home/user/backups/history.tar`
   - Uses the `watchdog` library to monitor the watch directory for any file creation or modification events matching `*.ini`.
   - Whenever an event occurs:
     a. Opens the modified `.ini` file and uses memory-mapped I/O (`mmap`) to read its contents.
     b. Decodes the contents from `ISO-8859-1` and encodes it to `UTF-8`.
     c. Computes a standard unified diff (using Python's `difflib.unified_diff`) between the previous UTF-8 content of the file (assume empty if it's a new file) and the new UTF-8 content. Use the filename for the "from" and "to" file headers in the diff.
     d. Writes this unified diff into a temporary file, then appends it to the uncompressed tar archive specified in the arguments (e.g., `history.tar`). The file inside the tar archive should be named `<filename>_<timestamp>.diff` (e.g., `app.ini_1690000000.diff`). You can use `int(time.time())` for the timestamp.
     e. Updates its internal state so the next modification computes the diff against this new version.

2. Once the script is ready, set up the environment:
   - Create the directories `/home/user/legacy_configs` and `/home/user/backups`.
   - Install `watchdog` if you haven't already.

3. Run your daemon in the background to watch `/home/user/legacy_configs` and archive to `/home/user/backups/history.tar`.

4. While the daemon is running, execute the simulation script located at `/home/user/simulate_changes.sh`. (You must create this script first based on the instructions below).
   - Create `/home/user/simulate_changes.sh` with the following content:
     ```bash
     #!/bin/bash
     echo -e "server=192.168.1.1\nport=8080" | iconv -f UTF-8 -t ISO-8859-1 > /home/user/legacy_configs/network.ini
     sleep 2
     echo -e "server=192.168.1.1\nport=8080\nenable_ssl=true" | iconv -f UTF-8 -t ISO-8859-1 > /home/user/legacy_configs/network.ini
     sleep 2
     ```
   - Make it executable and run it.

5. After the simulation finishes, gracefully terminate your Python daemon. 

Ensure that `/home/user/backups/history.tar` exists, is a valid tar file, and contains the two expected `.diff` files mapping the creation and subsequent modification of `network.ini`.