You are acting as a backup administrator. Your task is to write a Python script that automates the archiving, integrity checking, and monitoring of server logs. 

Write a Python script at `/home/user/backup_agent.py` that performs the following sequence of operations:

1. **Metadata-based File Search & Bulk Renaming:**
   - Scan the directory `/home/user/logs` (and its subdirectories) for `.log` files.
   - Identify files that meet AT LEAST ONE of these conditions:
     - Modified more than 7 days ago.
     - Size is strictly greater than 1 Megabyte (1,048,576 bytes).
   - For the identified files, rename them in their current directory by adding the prefix `archive_` to the filename, and replacing any spaces in the filename with underscores. (e.g., `web server.log` becomes `archive_web_server.log`).

2. **Archive Integrity Verification:**
   - Scan the directory `/home/user/archives` for all `.tar.gz` files.
   - Test each archive for integrity (i.e., whether it can be successfully decompressed/listed without errors).
   - Create a text file at `/home/user/corrupted_archives.txt`. Write the absolute paths of any corrupted `.tar.gz` files into this file, one path per line, sorted alphabetically. If no files are corrupted, create an empty file.

3. **File Watching and Change Detection:**
   - After completing the above steps, the script must monitor the directory `/home/user/incoming` for new `.log` files.
   - You may use a polling loop (e.g., using `os.listdir` and `time.sleep`) or a library like `watchdog`.
   - When a new `.log` file appears in `/home/user/incoming`, the script must immediately:
     - Rename it to `processed_<original_filename>`.
     - Move it into `/home/user/logs/`.
   - The script must keep running until it has successfully detected, renamed, and moved EXACTLY 3 `.log` files from the `/home/user/incoming` directory. Once the 3rd file is moved, the script should exit gracefully with code 0.

You must write the script and leave it at `/home/user/backup_agent.py`. Make sure the script runs and works correctly. You can test your script by running it and manually dropping files into the `/home/user/incoming` directory from another terminal.