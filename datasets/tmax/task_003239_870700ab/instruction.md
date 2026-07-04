You are acting as a Backup Administrator for a Linux system. We have a pipeline that automatically receives backup manifest files in JSON format from various users. These manifests specify which files should be included in the nightly archive.

However, we recently discovered a potential "zip slip" style vulnerability: some users have submitted manifests with paths containing directory traversal characters (`../`) or absolute paths pointing outside their restricted data directory, attempting to trick the archiver into backing up sensitive system files.

Your task is to write and execute a Python script that processes these manifests, followed by a shell command to summarize the results.

Here are the requirements:

1. **Input Directory**: Traverse recursively through `/home/user/backups/incoming/` to find all `.json` files.
2. **JSON Format**: Each JSON file has the following structure:
   ```json
   {
     "backup_id": "job-1234",
     "files": [
       "project/code.py",
       "../../../../etc/shadow",
       "/home/user/data/images/logo.png"
     ]
   }
   ```
3. **Validation Rule**: The allowed root directory for backups is strictly `/home/user/data/`. 
   - You must evaluate each file path in the `files` list.
   - If a path is relative, it is assumed to be relative to `/home/user/data/`.
   - If a path (after resolving all `../` and `./` components) falls strictly inside `/home/user/data/` (or is a descendant of it), it is **VALID**.
   - If a path resolves to a location outside `/home/user/data/` (e.g., `/etc/shadow`, `/home/user/other/file.txt`), it is **INVALID** and must be silently dropped.
4. **Atomic Write & CSV Output**: Write all VALID paths into a single CSV file located at `/home/user/backups/processed_manifest.csv`.
   - The CSV must have exactly two columns: `backup_id,valid_file_path`
   - The `valid_file_path` must be the fully resolved absolute path.
   - You **must** use an atomic write for this CSV. Write to a temporary file in the same directory first, then use an atomic rename (`os.replace` in Python) to move it to `/home/user/backups/processed_manifest.csv`. This prevents our concurrent cron jobs from reading a partially written file.
   - The CSV rows should be sorted alphabetically by `backup_id`, and then by `valid_file_path`.
5. **Text Transformation**: Once the Python script completes successfully, use a command-line text processing tool (`awk`, `sed`, or similar) to read `/home/user/backups/processed_manifest.csv`, extract only the unique `backup_id`s (skipping the header), and write them to `/home/user/backups/valid_ids.txt`, one per line, sorted alphabetically.

Ensure your Python script is robust and correctly handles the path resolution logic using libraries like `os.path` or `pathlib`. Write the script to `/home/user/process_backups.py` and run it.