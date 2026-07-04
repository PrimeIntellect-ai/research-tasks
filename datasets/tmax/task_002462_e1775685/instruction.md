You are tasked with organizing and auditing a chaotic configuration management system. 

Over the past year, various automated systems have dumped configuration backup files into the `/home/user/server_configs/` directory. These files are deeply nested, inconsistently named, and mixed with irrelevant files.

Your goal is to extract the active configurations, standardize their names, and generate an inventory log using Python and shell utilities. 

Here are the exact requirements:

1. **Locate Target Files:** Find all `.json` files inside `/home/user/server_configs/` (and its subdirectories) that were modified in the year 2023. Ignore files modified in any other year.
2. **Data Parsing:** Parse the contents of these specific files. Each valid configuration file is a JSON object containing at least the keys `"app_name"` (string) and `"config_version"` (string or float). Ignore any JSON files that do not contain BOTH of these keys.
3. **Bulk File Renaming & Organization:** For each valid configuration file found, copy it to a new directory `/home/user/active_configs/` and rename it to follow this exact format: `<app_name>_<config_version>.json`. All spaces in the `app_name` should be replaced with underscores (`_`) and it should be completely lowercase. (e.g., `{"app_name": "Web Server", "config_version": "2.4"}` becomes `web_server_2.4.json`).
4. **Atomic Write Inventory:** Create an inventory file at `/home/user/config_inventory.json`. This must be a JSON object mapping the normalized `app_name` to its `config_version` (e.g., `{"web_server": "2.4", "database": "1.0"}`). 
   * CRITICAL: The inventory file must be written atomically to avoid race conditions if another system reads it. You must write the output to a temporary file first (e.g., `/home/user/config_inventory.tmp.json`) and then use a standard atomic operation (like `os.replace()` in Python or `mv` in bash) to move it to the final destination `/home/user/config_inventory.json`.

Create the necessary directories, write a Python script (and any necessary bash commands) to perform this operation, and ensure the final state precisely matches the requirements.