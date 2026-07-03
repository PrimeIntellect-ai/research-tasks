You are tasked with writing a Python script to perform a safe, large-scale configuration update for a system tracking changes. 

System services are constantly reading from a complex, nested directory of configuration files located at `/home/user/app_configs`. We need to deprecate an old authentication configuration across all services while ensuring no race conditions occur during the updates, and preserving a backup of the original files.

Write a Python script at `/home/user/update_configs.py` that does the following:
1. Recursively traverses the `/home/user/app_configs` directory to find all files ending with the `.ini` extension.
2. For each `.ini` file found, acquire an exclusive file lock using the `fcntl` module (`fcntl.flock`) before reading or modifying it to prevent concurrent read/write issues.
3. Read the file. If the file contains the exact section header `[auth_v1]`, perform the following text replacements:
   - Replace `[auth_v1]` with `[auth_v2]`.
   - Within that section, change the exact string `token_expiry = 3600` to `token_expiry = 86400`.
4. If a file is going to be modified, add its original, unmodified content to a ZIP archive located at `/home/user/pre_update_backup.zip`. The paths in the ZIP archive should be relative to `/home/user/app_configs` (e.g., `serviceA/config.ini`).
5. Write the modified content back to the file and release the file lock.

Ensure the script can be executed directly from the terminal (e.g., `python3 /home/user/update_configs.py`) and completes the operation. Do not leave locks hanging.