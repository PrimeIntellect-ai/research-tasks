You are a developer tasked with securely organizing some incoming project files and creating a lightweight backup. 

You have received an archive located at `/home/user/incoming.zip`. We suspect this archive might have been poorly constructed or potentially malicious, containing "Zip Slip" directory traversal attempts (e.g., file paths containing `../` that attempt to write outside the extraction directory).

Please write and execute a Python script at `/home/user/safe_deploy.py` that performs the following steps:

1. **Safe Extraction**: Extract the contents of `/home/user/incoming.zip` into the directory `/home/user/project_data/`. You must programmatically inspect each file in the zip archive and **skip** extracting any file whose target absolute path falls outside of `/home/user/project_data/`. (Do not let it overwrite or write files outside this directory).
2. **Symlink Management**: After extraction, create a symbolic link at `/home/user/latest.txt` that points to the newly extracted `/home/user/project_data/valid_file.txt`.
3. **Hard-link Backup**: To simulate an incremental backup, copy the entire extracted contents of `/home/user/project_data/` to a new directory `/home/user/new_backup/`. To save space, the files in `/home/user/new_backup/` must be **hard links** to the files in `/home/user/project_data/`.

Requirements:
- Ensure the extraction strictly prevents directory traversal vulnerabilities.
- Run your script so the final state is applied to the filesystem.