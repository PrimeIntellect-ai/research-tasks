You are a storage administrator tasked with reclaiming disk space on a Linux server without losing critical error data. The application logs are currently taking up too much space. They are stored in JSON Lines (JSONL) format in the `/home/user/app_logs/` directory.

Your objective is to extract only the critical error logs, apply a custom dictionary-based compression to them, package them into an archive, and calculate the total disk space saved.

Here are your detailed instructions:

1. **Filter and Extract**:
   Read all `.jsonl` files in `/home/user/app_logs/`. Extract only the lines where the `"status"` is exactly `"FAILED"`.
   From these lines, extract the values of the `"timestamp"`, `"server_id"`, and `"error_code"` fields.

2. **Custom Compression (Dictionary Replacement)**:
   You have been provided with a dictionary file at `/home/user/dict.csv`. It contains comma-separated pairs: `original_string,short_code`.
   Replace the `server_id` and `error_code` values with their corresponding `short_code` from the dictionary.

3. **Format and Save**:
   For each processed log file, format the extracted, compressed data as a simple CSV with no header, in the order: `timestamp,short_server_id,short_error_code`.
   Save these condensed CSV files into the `/home/user/condensed_logs/` directory, keeping the original base filename but changing the extension to `.csv` (e.g., `server1.jsonl` becomes `server1.csv`).

4. **Archive and Cleanup**:
   Create an uncompressed tar archive of the `/home/user/condensed_logs/` directory at `/home/user/failed_logs_archive.tar`.
   After the archive is successfully created, delete the entire `/home/user/app_logs/` directory to free up disk space. Also, delete the `/home/user/condensed_logs/` directory.

5. **Calculate Savings**:
   Calculate the exact number of bytes saved. This is defined as:
   *(Total size in bytes of all original `.jsonl` files in `/home/user/app_logs/` BEFORE deletion)* - *(Total size in bytes of `/home/user/failed_logs_archive.tar`)*.
   Write this integer value to a file at `/home/user/space_saved.txt`.

Constraints:
- You must accomplish this using only Bash, standard shell built-ins, and coreutils (e.g., `sed`, `awk`, `grep`, `tar`, `stat`, `wc`). Do not use Python, Perl, or jq.
- Ensure the final tar archive extracts correctly to a `condensed_logs/` folder containing only the `.csv` files.