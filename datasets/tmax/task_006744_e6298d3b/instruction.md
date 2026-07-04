You are a storage administrator responsible for managing disk space on a Linux server. You need to build an automated archiving system that monitors a specific directory for archiving requests, parses those requests, finds matching files based on size metadata, and compresses them.

Your task is to create a Python script at `/home/user/watcher.py` and execute it in the background, then trigger it.

Here are the exact requirements for the system:

1. **Directories**: 
   Ensure the following directories exist (create them if they don't):
   - `/home/user/requests/`
   - `/home/user/archives/`

2. **The Watcher Script (`/home/user/watcher.py`)**:
   - The script should continuously monitor (poll every 2 seconds or use a file system watcher) the `/home/user/requests/` directory for new `.csv` files.
   - When a `.csv` file is detected (e.g., `batch1.csv`), the script must parse it. The CSV will not have a header row. Each row will contain two fields: `target_directory,min_size_bytes`.
   - For every row in the CSV, the script must search the `target_directory` (recursively) for all files that are **strictly larger** than `min_size_bytes`.
   - All matching files found from all rows in that CSV should be added to a single compressed tar archive (gzip) named `/home/user/archives/<csv_filename_without_extension>.tar.gz` (e.g., `/home/user/archives/batch1.tar.gz`). Inside the tarball, the files should retain their absolute paths.
   - After successfully creating the archive, the script must delete the triggering `.csv` file from the `/home/user/requests/` directory.

3. **Execution and Triggering**:
   - Run your `watcher.py` script in the background.
   - To prove your system works, create a file named `/home/user/requests/test_run.csv` containing exactly these two lines:
     ```
     /home/user/data/logs,4000
     /home/user/data/backups,15000
     ```
   - Wait for your script to process the CSV, create `/home/user/archives/test_run.tar.gz`, and delete the CSV.

**Note**: The directories `/home/user/data/logs` and `/home/user/data/backups`, along with various dummy files of different sizes, have already been created for you.