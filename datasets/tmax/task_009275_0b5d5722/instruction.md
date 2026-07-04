You are a storage administrator managing disk space and recovering data from a corrupted legacy backup. A previous rogue backup script followed symlinks recursively, creating infinite loops in the directory structure, and bundled various file formats together. 

Your task is to process this backup, extract specific data, and create a clean summary archive.

You have been provided with an archive at `/home/user/backup.tar.gz`. 

Write and execute a Python script (or bash commands) to perform the following steps:
1. Safely extract `/home/user/backup.tar.gz` into `/home/user/extracted/`. **Warning:** The archive contains a directory with a symlink loop (a symlink pointing to its parent directory). Make sure your traversal logic does not fall into an infinite loop!
2. Find all `.bin` files within the extracted contents (excluding any infinite symlink paths). Check their binary headers. Valid binary files in this system start with the 4-byte magic signature `0xEF 0xBE 0xAD 0xDE` (hex).
3. For each valid binary file, read the next 4 bytes immediately following the signature as an unsigned 32-bit integer (little-endian). This represents a timestamp. Write all extracted timestamps to `/home/user/binary_timestamps.txt`, one per line, in ascending numerical order.
4. Locate the `logs.zip` file within the extracted archive. Extract its contents to `/home/user/extracted_logs/`.
5. Find all `.json` files within the extracted logs. Each JSON file contains a list of records with the format: `{"id": <int>, "status": "<string>", "message": "<string>"}`.
6. Parse these JSON files and extract all records where the `status` is exactly `"ERROR"`.
7. Write these error records to a CSV file at `/home/user/summary.csv` with the header `id,status` and the corresponding data, sorted in ascending order by `id`.
8. Finally, create a new archive at `/home/user/final_report.tar.gz` containing exactly two files at its root level: `summary.csv` and `binary_timestamps.txt`.

Ensure all file paths and names match exactly as requested.