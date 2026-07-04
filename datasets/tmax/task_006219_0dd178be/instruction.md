You are a backup administrator recovering legacy application logs. We need to extract a specific log file from a nested backup archive, convert its character encoding to modern standards, and safely register its contents in a shared catalog using a C program. 

Please perform the following steps:

1. **Extract and Navigate**: 
   In `/home/user/backup_ops/`, there is a nested archive named `master_backup.tar.gz`. 
   Inside this tarball is a zip file named `logs_2022.zip`. Extract the tarball, then extract `logs_2022.zip` to find a file named `legacy_app.log`.

2. **Encoding Conversion**:
   The `legacy_app.log` file was written by an old system and is encoded in ISO-8859-1. Convert its encoding to UTF-8 and save the new file at `/home/user/backup_ops/legacy_app_utf8.log`.

3. **Data Extraction**:
   Count the number of lines in `/home/user/backup_ops/legacy_app_utf8.log` that contain the exact string `FATAL`.

4. **Safe Catalog Update (C Programming)**:
   Multiple administrators write to the backup catalog concurrently, so file locking is strictly required. 
   Write a C program at `/home/user/backup_ops/updater.c` that does the following:
   - Takes exactly one command-line argument: the count of FATAL lines you found.
   - Opens the file `/home/user/backup_ops/catalog.txt` in append mode.
   - Applies an exclusive file lock to the file (using `flock()` or `fcntl()`).
   - Appends the string exactly formatted as: `legacy_app_utf8.log recorded X FATAL events\n` (where X is the integer count passed as the argument).
   - Flushes/writes the data, releases the lock, and closes the file.
   
   Compile your C program to `/home/user/backup_ops/updater` and run it with the count you found.

Ensure the final compiled binary exists, the `catalog.txt` file has been safely updated, and the UTF-8 log file is placed exactly where specified.