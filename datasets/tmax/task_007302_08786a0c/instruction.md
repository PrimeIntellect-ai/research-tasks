You are acting as an assistant to a storage administrator who is trying to manage disk space by analyzing a large collection of nested backup archives. 

In `/home/user/old_backups`, there are several `.tar` files. Each of these `.tar` files contains multiple `.zip` files, and each `.zip` file contains various `.log` files. Some of these `.log` files are exact duplicates of each other across different archives.

Your task is to create a parallelized extraction and deduplication analyzer. 

**Requirements:**
1. **Python Script (`/home/user/analyzer.py`)**: 
   Write a Python script that accepts a single argument: the path to a `.tar` file.
   The script must:
   - Read the `.tar` file.
   - For every `.zip` file found inside the `.tar`, read the `.zip` file (preferably without extracting it to disk to save space, using `io.BytesIO` or similar).
   - For every `.log` file inside the `.zip`, compute the SHA-256 checksum of its uncompressed contents.
   - Update a central JSON manifest file located at `/home/user/dedup_manifest.json`.
   
   The `dedup_manifest.json` must have the following structure:
   ```json
   {
     "<sha256_hash>": [
       "<tar_filename>/<zip_filename>/<log_filename>",
       "<another_tar_filename>/<another_zip_filename>/<another_log_filename>"
     ]
   }
   ```
   If a file's hash already exists in the manifest, append the new path to the list. If it doesn't, create a new list with the path.

2. **File Locking & Concurrency**:
   Because there are many large archives, we need to process them in parallel. 
   When your Python script updates `/home/user/dedup_manifest.json`, it **must** use file locking (e.g., the `filelock` module or `fcntl`) to prevent data corruption from concurrent writes. If you use `filelock`, you may install it via `pip`. Read the current JSON, update the dictionary, and write it back, all while holding the lock. If the file doesn't exist yet, it should be created with an empty dictionary `{}` before updating. Use `/home/user/dedup_manifest.json.lock` as the lock file if using a separate lock file.

3. **Bash Runner (`/home/user/run_parallel.sh`)**:
   Write a bash script that finds all `.tar` files in `/home/user/old_backups` and runs `/home/user/analyzer.py` on each of them concurrently (in the background). The script must `wait` for all background processes to finish before exiting. Ensure the bash script has execution permissions.

You must write both `/home/user/analyzer.py` and `/home/user/run_parallel.sh` and ensure that running `/home/user/run_parallel.sh` successfully produces the complete, uncorrupted `/home/user/dedup_manifest.json`.