You are a storage administrator working to reclaim disk space on a critical Linux server. The system generates massive amounts of telemetry, which have been packaged into nested archives over time. Your goal is to parse these archives, remove verbose log levels to save space, and securely log your processing results.

In `/home/user/storage/`, there is a nested archive named `telemetry_logs.tar`. Inside this archive, there are several sub-archives (e.g., `.tar.gz` files), each containing a raw text log file.

Perform the following steps:
1. Extract all sub-archives from `/home/user/storage/telemetry_logs.tar`.
2. Extract the `.log` files from the nested sub-archives.
3. Parse each extracted `.log` file and remove any lines that contain the exact string `[TRACE]` or `[DEBUG]`. Leave all other lines intact.
4. Save the cleaned log files into the directory `/home/user/cleaned_logs/`, keeping their original filenames (e.g., `node1.log`).
5. Maintain a processing record in `/home/user/inventory.txt`. For every cleaned log file, append a line in the exact format: `<filename>,<new_line_count>` (e.g., `node1.log,450`).
6. **Concurrency constraint:** This server has automated background workers that also periodically append to `/home/user/inventory.txt`. To prevent race conditions and data corruption, you **must** use an exclusive file lock (e.g., using standard `flock` in bash or `fcntl` in Python) on `/home/user/inventory.txt` whenever you write to it. 

Complete this task using any combination of shell commands and scripts in a language of your choice.