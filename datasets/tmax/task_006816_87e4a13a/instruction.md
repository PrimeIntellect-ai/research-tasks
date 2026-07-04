You are a backup administrator tasked with archiving an influx of raw, unstructured data exports from various servers. 

Currently, there are several raw data files located in `/home/user/backups/raw/`. These files have inconsistent names (ending in `.txt`) and contain comma-separated values. 
Your objective is to process these files, transform their contents, rename them based on the data they contain, and generate a structured JSON manifest of the archive.

Please perform the following steps:

1. **Analyze and Rename:** For every `.txt` file in `/home/user/backups/raw/`, extract the "server name" and "date". 
   - The first line of each file is a header.
   - The second line is the first row of actual data. 
   - The first column is the server name, and the second column is the date (format: YYYYMMDD).
   - You must move and rename each file to `/home/user/backups/processed/<server_name>_<date>.csv`.

2. **Text Transformation:** While moving the files, convert the entire content of each file to completely lowercase. The final files in `/home/user/backups/processed/` must be entirely lowercase.

3. **Manifest Generation:** Create a JSON manifest file at `/home/user/backups/manifest.json`. The JSON file must have the following exact structure:
   ```json
   {
     "archives": [
       {
         "original": "old_filename.txt",
         "processed": "new_filename.csv",
         "checksum": "<sha256_hash_of_the_processed_lowercase_file>"
       },
       ...
     ]
   }
   ```
   *Note: The `original` field should only contain the basename of the original file (e.g., `data1.txt`), and `processed` should only contain the new basename (e.g., `web01_20231024.csv`). The checksum must be the SHA-256 hash of the final, lowercase `.csv` file.*

4. **Clean up:** Ensure the `/home/user/backups/raw/` directory is empty after processing.

You may use bash tools (awk, sed, jq, sha256sum, etc.) or write a script in a language of your choice (Python, Node, etc.) to accomplish this.