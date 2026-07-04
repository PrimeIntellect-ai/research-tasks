You are acting as a configuration manager tracking changes across our server. We have a backup directory at `/home/user/configs` containing various application configurations stored as `.zip` archives. Over time, some of these archives have become corrupted.

Your task is to write a Python script at `/home/user/tracker.py` that concurrently scans this directory tree, verifies the integrity of the archives, and logs the versions of the valid configurations.

Requirements for `/home/user/tracker.py`:
1. **Recursive Traversal**: Find all `.zip` files recursively inside `/home/user/configs`.
2. **Concurrent Processing**: Process the discovered `.zip` files concurrently using `concurrent.futures.ThreadPoolExecutor` or `ProcessPoolExecutor` with `max_workers=4`.
3. **Archive Verification**: For each `.zip` file, verify its integrity. If the archive is corrupt or invalid, skip it.
4. **Data Extraction**: If the archive is valid, check if it contains a file named `meta.json`. If it does, read the JSON and extract the value of the `version` key. If `meta.json` is missing, skip the archive.
5. **File Locking**: The workers must append their findings to a shared results file at `/home/user/tracking_results.csv`. To prevent race conditions from concurrent workers, you must use file locking (e.g., via `fcntl`) when writing to the CSV.
6. **Output Format**: Each appended line in `/home/user/tracking_results.csv` must be exactly in the format: `filename,version` (where `filename` is just the base name of the zip file, e.g., `backup.zip`, and `version` is the extracted version string). Do not write a header.

After writing the script, execute it so that `/home/user/tracking_results.csv` is populated. Ensure the script completes successfully.