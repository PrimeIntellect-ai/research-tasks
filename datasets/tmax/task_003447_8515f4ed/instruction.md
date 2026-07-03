I need a robust background service to organize and consolidate project metadata from multiple file formats into a single reliable index. 

Please write a Bash script at `/home/user/sync_projects.sh` that fulfills the following requirements:

1. **Initial Recursive Scan**:
   When the script starts, it should recursively search `/home/user/legacy_projects` for `.json` and `.csv` files.
   - JSON files have the structure: `{"id": 123, "project_name": "Alpha", "status": "active"}`
   - CSV files have a header `id,project_name,status` followed by data rows.
   - The script must extract the `project_name` and `status` from all these files.

2. **Atomic Index Creation**:
   Compile the extracted data into a single master JSON file located at `/home/user/master_index.json`. 
   The format must be a simple key-value map:
   ```json
   {
     "Alpha": "active",
     "Beta": "archived"
   }
   ```
   **Crucial**: To ensure safety for concurrent readers, any updates to `/home/user/master_index.json` MUST be atomic. You must write to a temporary file in the same directory first, then use `mv` to overwrite the original index.

3. **Continuous File Watching**:
   After the initial scan, the script must continuously watch the directory `/home/user/dropzone/` for new files being safely completely written (use `inotifywait` and listen for `close_write` events).
   When a new `.json` or `.csv` file is dropped into the dropzone, the script must parse it and update `/home/user/master_index.json` with the new `project_name` and `status`, again using atomic writes.

4. **Execution**:
   - You may need to install standard dependencies like `inotify-tools` or `jq` via `sudo apt-get` if they are missing (assume standard passwordless sudo for these package installs).
   - Make the script executable and run it in the background (`./sync_projects.sh &`). Leave it running so my automated system can drop test files into `/home/user/dropzone/` and verify the atomic updates.

Ensure the final JSON keys in `master_index.json` are properly formatted, uniquely combined, and valid JSON.