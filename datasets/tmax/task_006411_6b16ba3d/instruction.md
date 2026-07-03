You are acting as an artifact manager curating a binary repository. 

Your task is to write a Python script that continuously watches an incoming directory for new binary artifacts, verifies their archive integrity, parses their metadata, and routes them into a structured repository layout using symbolic links.

Here are the specific requirements:

1. Write a Python script at `/home/user/curator.py`.
2. The script must monitor the directory `/home/user/incoming/` for new `.tar.gz` files. You may use a simple polling loop (e.g., checking every 1 second).
3. When a new `.tar.gz` file is detected:
   a. Verify its gzip/tar archive integrity.
   b. If the archive is corrupted or invalid, append exactly the base filename (e.g., `broken.tar.gz`) to `/home/user/repo/corrupted.log` on a new line, and do not process it further.
   c. If the archive is valid, extract the `meta.json` file from within it.
   d. Parse `meta.json` to extract the `category`, `name`, and `version` fields.
   e. Create the appropriate canonical directory structure in the repository: `/home/user/repo/<category>/<name>/<version>/`.
   f. Create a symbolic link at `/home/user/repo/<category>/<name>/<version>/payload.tar.gz` that points to the absolute path of the original artifact in `/home/user/incoming/`.
   g. Ensure your script keeps track of processed files so it doesn't process the same file multiple times.

To test and complete this task:
1. Ensure `/home/user/incoming/` and `/home/user/repo/` exist.
2. Run your `/home/user/curator.py` script in the background.
3. Execute the provided script `/home/user/drop_artifacts.sh`. This script will simulate an external system dropping several archives (both valid and corrupted) into the incoming directory.
4. Wait at least 5 seconds for your curator script to process the files.
5. Terminate your background `curator.py` process.
6. Generate a summary of the symlinks by running the following command and saving its output exactly to `/home/user/repo/final_layout.txt`:
   `find /home/user/repo -type l | sort`

Ensure all paths in your Python script are absolute.