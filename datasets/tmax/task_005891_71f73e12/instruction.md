You are an AI assistant helping to manage an artifact curation system. 

Our upstream binary repository continuously writes metadata about uploaded artifacts into log files. These logs are rotated periodically. Due to a recent misconfiguration, the logs were written in UTF-16LE encoding, and the JSON entries have a formatting error: many lines end with a trailing comma after the closing brace `}`.

Your task is to create a C program and a supporting shell script to clean, parse, and transform this data.

Here are your instructions:

1. **Investigate the input:**
   The incoming log files are located in `/home/user/incoming/`. There are several rotated logs (e.g., `artifacts.log`, `artifacts.log.1`, etc.). 

2. **Write a C program:**
   Create a C program at `/home/user/curator.c`. 
   This program must:
   * Accept a directory path as a command-line argument.
   * Read all files starting with `artifacts.log` in that directory.
   * Read the contents, which are encoded in UTF-16LE, and convert them to standard UTF-8.
   * Clean up the formatting by removing any trailing commas at the very end of a JSON line (e.g., `{"id":"123","note":"héllo"},` -> `{"id":"123","note":"héllo"}`).
   * Parse the resulting JSON to extract two fields: `id` and `note`. (You may assume the JSON is completely flat and consistently formatted on a single line, so you can extract these fields using standard string manipulation functions in C without needing an external JSON library).
   * Append the extracted data to `/home/user/curated_artifacts.csv` in the format: `id,note`.

3. **Compilation:**
   Compile your C program to `/home/user/curator`. You may use standard libraries (like `iconv.h` for encoding conversion).

4. **Execution and Backup:**
   Write a bash script at `/home/user/process_and_backup.sh` that:
   * Runs `/home/user/curator /home/user/incoming`.
   * Creates an incremental tar backup of `/home/user/curated_artifacts.csv` into the directory `/home/user/backups/`. The backup file should be named `csv_backup.tar.gz`. If the backup archive already exists, use tar's update or append functionality (or use `rsync` to a staging folder and tar that) to incrementally backup the file.

Make sure the final `/home/user/curated_artifacts.csv` has standard UNIX newlines, is UTF-8 encoded, and accurately reflects the data from all the log files. Ensure the bash script is executable. Run your bash script to process the existing files.