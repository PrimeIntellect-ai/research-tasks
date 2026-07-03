I am a technical writer organizing documentation for our company's new line of CNC machines and their firmware updates. Our build system drops release artifacts as `.tar.gz` archives into a specific directory, but occasionally the network drops packets and corrupts the archives. I need you to create a Python script that automates my documentation prep workflow.

Write a Python script at `/home/user/process_releases.py` that does the following:

1. Scans the directory `/home/user/dropzone/` for all `.tar.gz` files.
2. Performs an archive integrity verification on each file. 
3. If an archive is corrupt or invalid, skip it and append the exact line `CORRUPT: <filename>` to `/home/user/process.log`.
4. If the archive is valid, extract it to a temporary directory and perform a metadata-based search to find:
   a. **ELF files:** Find all Linux ELF binaries (do not rely on file extensions, check the file signatures/magic bytes or use the `file` command). For each ELF file, determine its architecture (e.g., "ARM", "x86-64").
   b. **GCode files:** Find all `.gcode` files. Parse these domain-specific files to extract the print time. Look for a comment line that strictly starts with `; TIME:` and capture the value after it (e.g., `; TIME: 1h20m` -> `1h20m`).
5. Append a structured record of the valid release to a Write-Ahead Log (WAL) for our documentation database at `/home/user/doc_db.wal`. This must be in JSONL (JSON Lines) format. Each line should be a JSON object like this:
   `{"release": "<archive_filename>", "binaries": [{"name": "<filename>", "arch": "<architecture>"}], "gcode_times": [{"name": "<filename>", "time": "<time_string>"}]}`
   (Sort the `binaries` and `gcode_times` lists alphabetically by `name` to ensure consistency).
6. Perform an incremental backup by copying ONLY the valid `.tar.gz` files to `/home/user/archive_backup/`. You can use standard bash tools like `rsync` or `cp` invoked via Python, or native Python libraries.

Once you have written the script, execute it so that the files `/home/user/process.log`, `/home/user/doc_db.wal`, and the `/home/user/archive_backup/` directory are populated correctly based on the current contents of `/home/user/dropzone/`.