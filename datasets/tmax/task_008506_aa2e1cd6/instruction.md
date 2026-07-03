You are acting as a backup administrator managing incoming data archives. We have received a backup archive that is suspected of containing a "Zip Slip" vulnerability payload—a malicious attempt to overwrite files outside the intended extraction directory using path traversal sequences (like `../`) or absolute paths.

You need to safely process this archive and recover the latest configuration state from its contents.

Here are your instructions:

1. **Analyze and Safely Extract:**
   - You have been provided a ZIP archive located at `/home/user/data_backup.zip`.
   - Write a Python script to inspect the contents of this ZIP file without extracting it globally.
   - Identify any file paths within the ZIP that are malicious. A path is malicious if it is an absolute path (starts with `/`) or contains directory traversal sequences (e.g., `..`).
   - Write the exact malicious paths found in the archive into `/home/user/malicious_files.txt`, with one path per line.
   - Extract *only* the safe files into the directory `/home/user/safe_backup/`. Do not extract the malicious files.

2. **Reconstruct the Configuration:**
   - In the safely extracted files, you will find an initial configuration file named `config.ini` and several Write-Ahead Log (`.wal`) files.
   - The `config.ini` file represents the base state of a key-value dictionary. Ignore the `[Settings]` header; just treat the file as a set of key-value pairs.
   - The `.wal` files contain sequential transactions that mutate this configuration. The files should be processed in alphabetical order by their filename (e.g., `01.wal`, `02.wal`).
   - Each line in a `.wal` file represents an operation in the format: `[TXN_ID] [OPERATION] [KEY] [VALUE]` (Values might be empty for some operations).
   - Supported operations:
     - `SET [KEY] [VALUE]`: Sets or updates the KEY with the VALUE.
     - `DELETE [KEY]`: Removes the KEY from the configuration.
     - `APPEND [KEY] [VALUE]`: Appends VALUE to the existing string value of KEY. If KEY does not exist, treat it as a `SET`.
   - Apply all transactions in sequence to the base configuration from `config.ini`.
   
3. **Save the Result:**
   - Output the final, fully-resolved configuration as a JSON object (a single dictionary) formatted with 4-space indentation to `/home/user/final_config.json`.

Ensure your Python script cleanly handles the extraction, parsing, and JSON generation.