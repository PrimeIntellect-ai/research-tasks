You are a backup administrator responsible for preparing and archiving legacy server configuration data. 

You have been given access to a directory tree located at `/home/user/server_configs`. This directory contains various configuration files in JSON, XML, and CSV formats scattered across multiple subdirectories. Before you can run the daily incremental backup, you must normalize and update these files.

Please perform the following steps:

1. **Bulk Rename**: Traverse `/home/user/server_configs` and recursively rename all files so that their extensions are entirely lowercase (e.g., rename `.JSON` to `.json`, `.XML` to `.xml`, `.CSV` to `.csv`). Do not change the base name of the files.

2. **Data Parsing & Transformation**: Write a Python script to parse all the `.json` files in the directory tree. Look for any JSON file that contains the exact key-value pair `"status": "deprecated"` at the root level of the JSON object. 
   - For every file that matches this condition, modify the file in-place to change the value from `"deprecated"` to `"archived"`. You may use Python or tools like `sed`/`awk` for the text transformation, but the detection must use Python's JSON parsing.

3. **Manifest Creation**: Create a manifest file at `/home/user/manifest.csv`. This file should contain a single column listing the absolute file paths of all the JSON files you modified in step 2. Sort the file paths alphabetically.

4. **Incremental Backup**: After modifying the files, create an incremental backup of the `/home/user/server_configs` directory. A tar snapshot/metadata file from the previous full backup already exists at `/home/user/backup.snar`. Use `tar` with this snapshot file to create a gzipped incremental backup archive named `/home/user/incremental_backup.tar.gz`.

Ensure all tasks are executed with precise paths as specified.