You are acting as a backup administrator managing system archives. A set of compressed log files from various servers has been dumped into `/home/user/backup_data/raw_logs/`. You need to extract critical events, safely consolidate them, and mark the files as processed. 

Because the dataset in a real environment would be massive, you must write a Python script `/home/user/archive_processor.py` to automate this task using concurrent processing.

Your Python script must meet the following exact requirements:
1. **Target Directory**: Process all `.log.gz` files located in `/home/user/backup_data/raw_logs/`.
2. **Compressed Stream Processing**: Read the contents of the gzip files on-the-fly without permanently extracting them to disk.
3. **Data Parsing**: Identify any log line that contains the exact string `[CRITICAL]`.
4. **Concurrent Execution & File Locking**: Use Python's `multiprocessing` or `concurrent.futures` (with multiple processes/workers) to process the files concurrently. All workers must append the identified critical lines to a single shared output file: `/home/user/critical_events.txt`. To prevent data corruption from concurrent writes, you must implement file locking (e.g., using `fcntl`) when writing to the shared file.
5. **Bulk Renaming**: Immediately after a `.log.gz` file is successfully parsed and its critical lines are written, rename the file to replace the `.log.gz` extension with `.archived.gz` in the same directory.

Run your script to complete the task.

Success is achieved when:
- `/home/user/critical_events.txt` contains every `[CRITICAL]` line from all the logs, with no garbled or overlapping text.
- All original `.log.gz` files have been renamed to `.archived.gz`.
- The script uses concurrency and proper file locking.