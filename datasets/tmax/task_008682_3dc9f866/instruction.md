You are a storage administrator managing disk space on a Linux server. An application has dumped several raw log fragments into the `/home/user/raw_logs/` directory. These files are poorly named and taking up space on the active volume.

Your task is to transform, bulk rename, and migrate these files to a new directory while logging the process.

Requirements:
1. Read each `.raw` file in `/home/user/raw_logs/`. Inside each file, the first line always contains a date in the format: `REPORT_DATE=YYYY-MM-DD`.
2. Move each file to the `/home/user/cold_storage/` directory.
3. While moving, change the file extension from `.raw` to `.log`, and prepend the extracted date to the filename. 
   * Example: If `fragment_test.raw` contains `REPORT_DATE=2023-10-01`, it should be moved and renamed to `/home/user/cold_storage/2023-10-01_fragment_test.log`.
4. Create a migration report at `/home/user/migration.log` using standard stream redirection. For every file processed, append a line to this log in the exact format: `[old_filename] -> [new_filename]`. 
   * Example: `fragment_test.raw -> 2023-10-01_fragment_test.log`
5. The entries in `/home/user/migration.log` must be sorted alphabetically by the old filename.

You may use any language (e.g., Python, Bash) to accomplish this task. Ensure that the original `/home/user/raw_logs/` directory is empty of `.raw` files once you are finished.