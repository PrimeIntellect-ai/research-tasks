You are helping a developer safely organize and process a batch of project files that were packaged poorly by a legacy system. 

You have been provided with an archive at `/home/user/corrupt_data.tar`. This archive is known to contain "tar slip" vulnerabilities—members with absolute paths or `../` sequences that attempt to write outside the intended extraction directory. 

Please complete the following steps:

1. **Safe Extraction**: Write a Python script at `/home/user/safe_extract.py` that reads a tar archive from standard input (stdin) and extracts it safely to a target directory passed as the first command-line argument. The script must neutralize any path traversal attempts (e.g., `../` or absolute paths) by stripping out the unsafe components and forcing all files to be extracted strictly within the target directory. 
   Run your script as follows: `cat /home/user/corrupt_data.tar | python3 /home/user/safe_extract.py /home/user/safe_output`

2. **File Merging**: The extracted archive contains a directory `safe_output/logs/` with a split log file (`app.log.aa`, `app.log.ab`, `app.log.ac`). Merge these chunks in alphabetical order into a single file at `/home/user/final_data/app_complete.log`.

3. **Bulk Renaming**: Inside `safe_output/data/`, there are several files named `metric_<id>.data` (e.g., `metric_xyz.data`). Move them to `/home/user/final_data/` and rename them all to change the extension from `.data` to `.csv` and prepend `processed_` to the filename (e.g., `processed_metric_xyz.csv`).

4. **Differential Backup**: A base backup of the final data directory exists at `/home/user/base_backup/`. Use standard Linux tools (like `rsync` or `tar`) to create a differential backup archive of `/home/user/final_data/` relative to `/home/user/base_backup/`. Save this archive at `/home/user/diff_backup.tar` containing only the files that are new or changed.

Make sure all directories exist (create `/home/user/final_data/` if needed).