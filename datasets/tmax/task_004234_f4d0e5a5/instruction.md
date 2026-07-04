I need you to help me organize my project files by creating a custom differential backup script in Python. 

I have a project directory at `/home/user/project` and a previous backup archive at `/home/user/backup_v1.tar.gz`. A live application has continued to write logs and modify binary files since the first backup.

Write and execute a Python script at `/home/user/make_backup.py` that performs the following tasks:
1. Opens and verifies `/home/user/backup_v1.tar.gz`.
2. Compares the files in `/home/user/project` against the contents of the archive.
3. Creates a new differential backup archive at `/home/user/backup_v2.tar.gz`.

The new archive `/home/user/backup_v2.tar.gz` must contain:
- Only files that have been modified or are new compared to `backup_v1.tar.gz`. If a file's binary content is identical to the one in the archive, do not include it.
- For the log file `app.log`: parse it and extract ONLY the new log lines that were appended after the last line present in the archived version of `app.log`. Save these new lines into the archive under the name `app_diff.log` (do not include the entire `app.log`).

You can use standard Python libraries (`tarfile`, `hashlib`, etc.). Ensure the script runs successfully and generates `/home/user/backup_v2.tar.gz` with exactly the required differential contents.