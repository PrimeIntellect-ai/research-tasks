You are helping me organize and modernize my old project files. I have a directory containing legacy project data at `/home/user/old_projects`, and a backup directory that is mimicking a mounted drive at `/home/user/backup_drive/projects_backup`. The backup is currently out of date.

Your task is to perform the following operations:

1. **Incremental Backup**: First, use a standard Linux tool to perform an incremental backup, syncing the contents of `/home/user/old_projects/` to `/home/user/backup_drive/projects_backup/`. Ensure that only new or modified files are copied, and the directory structure is preserved exactly.

2. **Format Conversion & Traversal**: Write and execute a Python script at `/home/user/transform_projects.py` that recursively traverses the `/home/user/old_projects` directory. 
   - Whenever it encounters a `.csv` file, it must read the CSV (which will have headers) and convert it into a `.json` file in the same directory.
   - The resulting `.json` file must have the exact same base name (e.g., `data.csv` becomes `data.json`), and its content should be a JSON array of dictionaries, where each dictionary represents a row mapping the CSV headers to their respective row values.
   - After successfully creating the JSON file, the script must delete the original `.csv` file.
   - Do not modify any existing `.json` files that were already in the directory.

3. **Logging**: Your Python script must keep track of every *new* `.json` file it created during this process. Have it write the absolute paths of all newly created `.json` files to `/home/user/conversion_log.txt`. The paths must be sorted alphabetically, with one path per line.

Ensure your Python script works flawlessly and runs to completion.