You are building the core processing script for a configuration manager that tracks and normalizes incoming configuration drops. 

Various applications drop their configuration files into `/home/user/incoming_configs/`. These files can be in JSON, XML, or CSV format. Your task is to write a Python script at `/home/user/config_manager.py` that processes these files, standardizes their names, and moves them to `/home/user/processed_configs/`.

Here are the requirements for `/home/user/config_manager.py`:
1. It must iterate through all files in `/home/user/incoming_configs/`.
2. It must parse each file to extract two specific values: the application name (`app_name`) and the version (`version`).
   - For JSON files (`.json`): Extract the `app_name` and `version` top-level keys.
   - For XML files (`.xml`): Extract the text content of the `<app_name>` and `<version>` tags (assume they are direct children of the root element).
   - For CSV files (`.csv`): Extract the `app_name` and `version` from the first data row (the first row is the header, determining the column indices).
3. It must move and rename the file into the `/home/user/processed_configs/` directory. The new filename must follow the format: `{app_name}_v{version}.{original_extension}`.
4. It must log its actions by writing to `/home/user/sync_log.txt`. For each processed file, write exactly one line in the following format:
   `[WATCHER] {original_filename} moved to {app_name}_v{version}.{original_extension}`
5. The entries in `/home/user/sync_log.txt` MUST be sorted alphabetically by the `{original_filename}`. (You can collect the log lines and sort them before writing to the file).

After writing the script, execute it so that the current files in `/home/user/incoming_configs/` are successfully processed, moved, and logged.