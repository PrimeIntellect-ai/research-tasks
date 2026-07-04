I need you to help me organize and back up some research datasets. I have a messy directory structure with some corrupted symlinks that cause infinite loops if traversed carelessly. 

Please write and execute a Python script to perform an incremental backup of my data based on the following requirements:

1. **Parse the Update Log:**
   Read the multi-line log file located at `/home/user/dataset_updates.log`. 
   The log contains blocks like this:
   ```
   [YYYY-MM-DD HH:MM:SS]
   Dataset: <Dataset_ID>
   Status: <SUCCESS|FAILED>
   Details: <Some description>
   ```
   Identify all `Dataset_ID`s that have a `Status: SUCCESS`. Ignore any that have `FAILED`.

2. **Search and Handle Symlinks:**
   The dataset directories are located in `/home/user/research_data/`. 
   For each successful dataset ID, search its corresponding subdirectory (e.g., `/home/user/research_data/<Dataset_ID>/`) for data files ending in `.json` or `.xml`. 
   *Warning:* My previous scripts created cyclic directory symlinks inside these folders. Your script must safely find all `.json` and `.xml` files without getting caught in infinite directory traversal loops. If a `.json` or `.xml` file is itself a symlink, you should read its target.

3. **Format Conversion:**
   Convert the found `.json` and `.xml` files into a standardized `.csv` format. 
   - `.json` files contain a JSON array of dictionaries (e.g., `[{"id": 1, "value": "A"}, ...]`).
   - `.xml` files contain records in this format: `<dataset><record><id>1</id><value>A</value></record>...</dataset>`.
   The resulting CSV files should have a header row with the keys, followed by the data rows. Name the output CSV files `<Dataset_ID>.csv` and save them temporarily in `/home/user/backup_staging/` (create this directory if it doesn't exist).

4. **Archive Creation:**
   Compress all the generated `.csv` files from `/home/user/backup_staging/` into a single gzipped tarball located at `/home/user/incremental_backup.tar.gz`. The tarball should not contain the absolute path `/home/user/backup_staging/` in its structure; the CSV files should be at the root of the archive.

Please complete this task using Python. Let me know when the tarball is ready.