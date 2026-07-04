You are acting as an automated configuration manager. We receive daily configuration backups as nested archives, and we need to process them to track changes properly. 

There is an incoming backup archive located at `/home/user/incoming_configs.tar.gz`. This archive contains several `.zip` files, which in turn contain text configuration files (`.conf`) and binary assets.

Your task is to write and execute a Python script (you can name it `/home/user/process.py`) that performs the following operations:
1. Extract the outer archive `/home/user/incoming_configs.tar.gz`.
2. Find and extract all nested `.zip` files.
3. Locate all `.conf` files across the extracted contents.
4. For each `.conf` file:
   - Read the file as text.
   - Prepend the exact string `# MANAGED BY CONFIG_TRACKER v2.0\n` to the beginning of the file.
   - Rename the file by appending `_tracked` before the extension (e.g., `settings.conf` becomes `settings_tracked.conf`).
5. Create a new archive at `/home/user/processed_configs.tar.gz` containing *only* the newly renamed `*_tracked.conf` files. You can store them flat or preserve the directory structure, as long as all the tracked `.conf` files are included in the root or subdirectories of the new `.tar.gz`.

Do not include any binary files (like `.bin` or `.png`) in the final archive.