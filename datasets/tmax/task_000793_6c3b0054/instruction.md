You are an IT backup administrator. You need to write a Python script that automates a secure log archiving process based on rules defined in a configuration file.

Write a Python script at `/home/user/archiver.py` that does the following:

1. Reads the JSON configuration file located at `/home/user/backup_config.json`.
2. Parses the configuration which contains the following keys:
   - `target_dir`: The directory to recursively search for log files.
   - `min_days_old`: The minimum age of the files in days (based on last modification time) to be considered for archiving.
   - `mask_regex`: A regular expression pattern for sensitive data (e.g., email addresses) that must be redacted.
   - `mask_replacement`: The string to replace the sensitive data with.
   - `archive_path`: The absolute path where the final ZIP archive should be saved.
3. Finds all files within `target_dir` (and its subdirectories) that were modified strictly more than `min_days_old` days ago from the time the script runs. (Assume exactly 24 hours per day. So `> min_days_old * 86400` seconds older than the current time).
4. Reads the contents of each matching file and redacts any text matching the `mask_regex` by replacing it with the `mask_replacement` string.
5. Archives the redacted files into a standard ZIP file at the location specified by `archive_path`. The internal paths in the ZIP file should be relative to `target_dir` (e.g., if a file is at `/home/user/app_logs/subdir/log1.txt` and `target_dir` is `/home/user/app_logs`, its path inside the zip should be `subdir/log1.txt`).
6. After successfully adding them to the archive, the script should permanently delete the original matching log files from the disk.

Do not modify files that do not meet the age criteria. Your script must be self-contained and run successfully when executed via `python3 /home/user/archiver.py`. Execute the script once you have written it to complete the task.