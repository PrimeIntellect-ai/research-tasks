You are acting as a backup administrator. We need to implement a robust data archiving tool in Python that reads a backup configuration file, sanitizes sensitive log data, and packages the result into a compressed archive.

Your task is to write a Python script at `/home/user/backup_tool.py` and then run it.

Here are the requirements:

1. **Prerequisites**: 
   - You must install the `pyyaml` package.
   - The backup configuration will be located at `/home/user/backup_config.yaml`. (Assume this file already exists with the configuration details).
   - Source files are located in `/home/user/data_source/`.
   - The output archive directory is `/home/user/backups/`. You must create this directory.

2. **The Python Script (`/home/user/backup_tool.py`)**:
   - Must parse `/home/user/backup_config.yaml`. The YAML file contains:
     ```yaml
     archive_name: "/home/user/backups/sanitized_backup.tar.gz"
     source_directory: "/home/user/data_source"
     anonymize_logs: true
     include_db: true
     ```
   - Must iterate through all files in `source_directory`.
   - If `anonymize_logs` is true, any file ending with `.log` must have all IPv4 addresses (e.g., `192.168.1.50`) replaced with `XXX.XXX.XXX.XXX` before being archived. *Do not modify the original files in `source_directory`.*
   - If `include_db` is true, files ending in `.sql` should be included in the archive without modification.
   - The script must create a `tar.gz` archive at the path specified by `archive_name`. 
   - Inside the archive, the files should be at the root level (no parent directories).
   - The script must print the name of each file added to the archive to standard output (e.g., "Added access.log").
   - If a file is skipped or an error occurs, print a warning to standard error.

3. **Execution**:
   - Run your script using standard stream redirection to save the standard output to `/home/user/backup.out` and standard error to `/home/user/backup.err`.

Ensure the final archive is correctly formatted and contains the sanitized data.