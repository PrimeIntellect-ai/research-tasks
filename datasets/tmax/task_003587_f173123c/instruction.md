You are a storage administrator tasked with optimizing disk space on a logging server. Several applications write log files to directories in `/home/user/logs/`, but the files are in mixed formats, mixed encodings, and often contain duplicate data.

Your goal is to write and execute a Python script at `/home/user/storage_optimizer.py` that normalizes these files and deduplicates them using hard links. 

Here are the requirements for your script:
1. Read the configuration file at `/home/user/config.yaml`. It contains a key `directories` (a list of paths to process) and `target_format` (which will be `json`).
2. Iterate through all files in the configured directories. For each file, you must acquire an exclusive lock using `fcntl.flock(fd, fcntl.LOCK_EX)` before reading and modifying it to prevent corruption from concurrent writers. Release the lock when done.
3. Detect the character encoding of each file. If it is not UTF-8 (e.g., UTF-16LE or ISO-8859-1), convert the content to UTF-8.
4. Detect the format of each file. If the file is a CSV, convert its contents to JSON (a JSON array of objects, where keys are the CSV headers). Save the new JSON content into a new file with the `.json` extension, and delete the original `.csv` file. If the file is already JSON, just ensure it is in UTF-8.
5. After all files are normalized to UTF-8 JSON, identify files with exactly identical content.
6. Replace duplicate files with hard links. For any set of identical files, keep the one that comes first alphabetically by its full path, and replace the others with hard links to it.
7. Generate a final report at `/home/user/optimizer_report.json` with the following exact JSON structure:
   ```json
   {
     "total_files_processed": <int>,
     "csv_to_json_conversions": <int>,
     "hard_links_created": <int>
   }
   ```

Write the script, run it, and verify that the space has been optimized and the report generated.