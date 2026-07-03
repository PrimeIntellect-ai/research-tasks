You are tasked with recovering and processing a fragmented backup that contains an infinite symlink loop. 

A legacy backup system generated a multi-part tar archive located at `/home/user/backups/`. The files are named `raw_backup.tar.gz.partaa` and `raw_backup.tar.gz.partab`.

Unfortunately, the directory structure inside the backup contains looping symbolic links, as well as hard links to the same files.

Your task is to:
1. Reassemble and extract the multi-part archive into `/home/user/extracted_backup/`.
2. Write a Python script at `/home/user/process.py` that traverses the extracted directory to find all `.json` files.
3. Your script must safely handle the infinite symlink loops (do not get trapped) and avoid processing the same physical file more than once (account for hard links and symlinks pointing to the same file).
4. Parse the valid JSON files. Each file contains a JSON array of objects with the keys `id` (integer), `name` (string), and `timestamp` (string).
5. Aggregate all unique records from all unique JSON files and sort them in ascending order by their `id`.
6. Split (chunk) the sorted records and write them to CSV files in the directory `/home/user/processed_csv/`. Each CSV file should contain exactly 3 records (except the last one, which will contain the remainder). Name the files `chunk_0.csv`, `chunk_1.csv`, etc.
7. The CSV files must include a header row: `id,name,timestamp`.
8. **Crucial:** To prevent data corruption in case of a crash, your Python script must use **atomic writes** when creating the CSV files. You must write the chunk data to a temporary file in the same directory first, and then atomically rename it to the final `chunk_X.csv` filename.

Ensure your script is executable or runnable via `python3 /home/user/process.py`. When you are finished, the final CSV files must perfectly reflect the sorted, deduplicated JSON data.