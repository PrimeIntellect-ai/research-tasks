You are tasked with helping a storage administrator solve a disk space management issue caused by a legacy application. The application writes logs rapidly and rotates them unpredictably, causing a race condition where log processors miss data or read incomplete files. 

You must create a robust C++ log watcher and transformer that monitors the log directory, safely captures completed rotated logs, extracts critical errors, maintains a checksum manifest, and updates a "latest" symlink.

**Requirements:**
1. **Directories**: 
   - Raw logs are written to: `/home/user/raw_logs/`
   - Processed logs must go to: `/home/user/processed_logs/`
   - You must create `/home/user/processed_logs/` if it does not exist.

2. **The C++ Watcher Program**:
   - Write a C++ program at `/home/user/log_watcher.cpp`.
   - The program must use Linux `inotify` to monitor the `/home/user/raw_logs/` directory.
   - It should detect when a rotated log file is completely written and closed (e.g., `IN_CLOSE_WRITE` or `IN_MOVED_TO` depending on how the application rotates). Only process files matching the naming pattern `app.log.*` (e.g., `app.log.1`, `app.log.2`). Ignore `app.log` (the active writer file).
   
3. **Multi-line Log Parsing**:
   - The log files contain multi-line entries. Every entry begins with `[` (e.g., `[INFO]`, `[ERROR]`, `[DEBUG]`).
   - Your C++ program must extract *only* the `[ERROR]` log entries, including all subsequent lines associated with that error (up to the next line starting with `[` or the end of the file).
   
4. **Transformation & Output**:
   - For every processed log file (e.g., `app.log.1`), create a file `/home/user/processed_logs/error_app.log.1`.
   - Write the extracted multi-line errors into this file exactly as they appeared. If there are no errors, create an empty file.
   - Calculate the SHA256 checksum of the resulting `error_app.log.*` file.
   - Append the checksum to a manifest file at `/home/user/processed_logs/manifest.txt` in standard format: `<checksum>  <filename>` (just the base filename, e.g., `error_app.log.1`).
   - Create or update a symbolic link at `/home/user/processed_logs/latest_error.log` pointing to the newly created `error_app.log.*` file.

5. **Execution flow**:
   - Write and compile your C++ program (`g++ -std=c++17 /home/user/log_watcher.cpp -o /home/user/log_watcher`).
   - Run your watcher in the background (`/home/user/log_watcher &`).
   - We have provided a log generation script at `/home/user/simulate_writer.sh`. Execute this script (it takes about 5 seconds to run) while your watcher is running. It will simulate the application writing and rotating logs.
   - Once the script finishes, cleanly terminate your watcher program (e.g., `kill %1` or via `pkill log_watcher`).

Verify that your `/home/user/processed_logs/manifest.txt` contains the correct checksums and that the `latest_error.log` symlink points to the highest numbered processed log.