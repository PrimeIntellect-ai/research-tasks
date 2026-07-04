You are a Cloud Architect migrating a legacy on-premise service to a modern simulated cloud environment. You need to automate the extraction of data from a legacy interactive tool and create a "cloud-native" mount structure using symbolic links based on a configuration file.

Here is the situation:
1. There is a legacy export tool at `/home/user/legacy_export.py`. When run manually, it prompts interactively:
   - "Enter admin password: " (The password is: `cloud_admin_99`)
   - "Enter export path: " (You should provide: `/home/user/export_data`)
   It will then create the exported data directories.

2. There is a configuration file at `/home/user/migration_fstab` that maps the exported directories to their new "cloud mount" locations. The file has the format:
   `<source_directory_name> <target_symlink_path>`
   (Lines starting with `#` are comments and should be ignored).

Your task:
1. Write a Python script at `/home/user/run_export.py` that uses the `pexpect` library to automate the execution of `/home/user/legacy_export.py`. It must supply the correct password and export path, wait for completion, and exit gracefully. (You may need to install `pexpect` via pip).
2. Write a robust, **idempotent** Python script at `/home/user/setup_mounts.py` that reads `/home/user/migration_fstab`. For each valid line, it should:
   - Ensure the parent directory of the `<target_symlink_path>` exists.
   - Create a symbolic link at `<target_symlink_path>` pointing to `/home/user/export_data/<source_directory_name>`.
   - Ensure the script handles the case where the link or target already exists without failing (idempotency).
3. Execute both scripts so the data is exported and the symlinks are correctly established.
4. Once successfully completed, create a log file at `/home/user/migration_status.log` containing exactly the string: `MIGRATION_COMPLETE`.