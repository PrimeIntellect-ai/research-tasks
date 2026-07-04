You are acting as a backup administrator. We have an application that continuously updates its configuration and status to a file. We need to safely read and archive this file without getting corrupted reads if the application writes to it simultaneously. 

Your objective is to write a Python script that safely reads the live file, transforms it to redact sensitive information, and outputs the result to standard output, which you will then pipe to an archive file.

Here is the setup:
1. There is a configuration rule file located at `/home/user/backup_rule.json` which contains JSON data specifying the source file and the key to redact:
   `{"source": "/home/user/settings.conf", "mask_key": "SECRET_TOKEN"}`
2. The live file is located at `/home/user/settings.conf`.

Write a Python script at `/home/user/archive_config.py` that does the following:
1. Reads `/home/user/backup_rule.json` to extract the `source` file path and the `mask_key`.
2. Opens the `source` file and acquires a shared lock on it using the `fcntl.flock(file, fcntl.LOCK_SH)` method to ensure concurrent writes are paused during the read.
3. Reads the file line by line.
4. For any line that begins with exactly the `mask_key` followed by an equals sign (e.g., `SECRET_TOKEN=somevalue`), modifies the line so the value is replaced entirely with `***` (e.g., `SECRET_TOKEN=***`). 
5. Retains all other lines exactly as they are.
6. Prints the resulting transformed lines to `stdout`.
7. Releases the lock and closes the file.

Once you have written the script, execute it in the terminal and redirect its standard output to create the final archive file at `/home/user/archived_settings.conf`.

Make sure your script correctly implements the file locking mechanism and that the final output file `/home/user/archived_settings.conf` is successfully generated with the redacted data.