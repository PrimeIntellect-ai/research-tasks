I need you to write a custom incremental backup utility in Python to help organize and archive my project workspace. I have a directory at `/home/user/project_workspace` containing source code, data, and log files. 

Please create a Python script at `/home/user/smart_archiver.py` that fulfills the following requirements:

1. **CLI Arguments**: The script should accept exactly three positional arguments:
   `python3 /home/user/smart_archiver.py <source_dir> <output_archive.tar> <state_file.json>`

2. **Incremental Backup Logic**:
   - The script must traverse the `<source_dir>` and all subdirectories.
   - It should read `<state_file.json>`, which contains a JSON dictionary mapping relative file paths to their last modification timestamp (floating point or integer). If the state file doesn't exist, treat it as an empty dictionary (a full backup).
   - A file should only be included in the backup if its relative path is not in the state file, or if its current modification time is strictly greater than the time stored in the state file.
   - After processing, the script must write the updated state back to `<state_file.json>`, containing the relative paths and their new modification times for *all* current files in the directory.

3. **Archive Creation and Stream Processing**:
   - The output should be an uncompressed tar archive (`.tar`).
   - For any file being backed up that ends in `.log` or `.txt`, you must NOT add the file directly. Instead, read its contents, compress the data stream using the `gzip` algorithm, and add the compressed data to the tar archive. The file's path inside the tar archive must have `.gz` appended to it (e.g., `logs/app.log` becomes `logs/app.log.gz` in the archive).
   - All other files (e.g., `.py`, `.json`) should be added to the tar archive normally without compression and without changing their names.

Once you have written the script, please execute the following steps to demonstrate it works:
1. Run a full backup: 
   `python3 /home/user/smart_archiver.py /home/user/project_workspace /home/user/full_backup.tar /home/user/state.json`
2. Simulate developer activity by doing two things:
   - Create a new file at `/home/user/project_workspace/src/new_module.py` with the content `print("Hello World")`
   - Append the line `ERROR: Connection timeout` to `/home/user/project_workspace/logs/server.log`
3. Run an incremental backup:
   `python3 /home/user/smart_archiver.py /home/user/project_workspace /home/user/incr_backup.tar /home/user/state.json`

Ensure all tar archives and the JSON file are located exactly where specified.