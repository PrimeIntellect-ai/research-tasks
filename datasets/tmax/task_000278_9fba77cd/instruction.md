I have a massive directory of project logs located at `/home/user/project_logs/`. These logs are highly nested JSON files. I need your help to parse them efficiently, extract critical metrics, and set up an incremental backup system.

Here is what I need you to do:

1. **Fix and Install the Parser:**
   I want to use the `ijson` library for iterative JSON parsing because the files can get very large. I have vendored the source code for `ijson` at `/app/ijson-vendored`. However, when I install it using `pip install -e /app/ijson-vendored`, the parsing is extremely slow. I suspect the C-extension (`yajl2` backend) isn't building due to a bug or misconfiguration in the package's `setup.py`. 
   Fix the vendored package so that the fast C-extension builds correctly, and install it in the system environment.

2. **Write the Parsing Script (`/home/user/parse_logs.py`):**
   Write a Python script that recursively traverses `/home/user/project_logs/`. For every `.json` file it finds, use `ijson` to parse the file iteratively. 
   The JSON files contain arrays of objects. You need to look for objects where the `"severity"` key equals `"CRITICAL"`. For those objects, extract the `"error_code"` (an integer). 
   Aggregate the total count for each unique `error_code` across all files.
   Write the aggregated results to `/home/user/summary.csv` with the header `error_code,count`, sorted by `error_code` in ascending order.
   *Performance requirement:* The script must process the data extremely fast. If the C-extension for `ijson` is working, it should easily run in under 1.5 seconds. If it uses the pure Python fallback, it will be too slow and fail the performance metric.

3. **Create an Incremental Backup Script (`/home/user/backup.sh`):**
   Write a bash script that takes two arguments: a source directory and a backup destination directory. 
   Usage: `./backup.sh /home/user/project_logs /home/user/backups`
   The script must use `rsync` to perform an incremental backup. It should create a new timestamped folder inside the destination (e.g., `/home/user/backups/2023-10-25T10:00:00/`) and use the `--link-dest` flag pointing to the most recent previous backup in that destination to save disk space.

Please ensure all scripts are executable and work correctly. Do not use external libraries other than the vendored `ijson` for parsing.