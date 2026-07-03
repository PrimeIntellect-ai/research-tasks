You are tasked with writing a Bash script that acts as a configuration manager tracking changes across different formats. 

There is a directory `/home/user/configs/` containing various configuration files in JSON, CSV, and XML formats. Some of these files have been modified recently, while others are old.

Write a Bash script at `/home/user/track_configs.sh` that does the following:
1. Finds all files in `/home/user/configs/` that have been modified within the last 24 hours.
2. For each recently modified file, extracts its version string:
   - For `.json` files: The file will contain a `"version": "X.Y.Z"` key-value pair. Extract the value.
   - For `.csv` files: The file has two columns. Find the row where the first column is exactly `version` and extract the value from the second column.
   - For `.xml` files: Extract the text content strictly between the `<version>` and `</version>` tags.
3. Appends the results to a central tracker file located at `/home/user/config_inventory.txt` in the format `filename:version` (e.g., `app_new.json:1.2.3`). Do NOT include the full directory path in the filename, just the basename.
4. Uses `flock` (file locking) to obtain an exclusive lock on `/home/user/config_inventory.txt` while appending to it, to prevent race conditions from simulated concurrent executions.

After writing the script, ensure it is executable and run it once so that `/home/user/config_inventory.txt` is populated.