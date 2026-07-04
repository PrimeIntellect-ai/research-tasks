You are acting as a backup administrator managing a custom archiving system. You need to write a Python tool to archive system logs using a proprietary format, a custom data transformation (simulating a custom compression pre-processing step), and safe atomic writes to prevent corrupted backups.

Your task is to create a Python script at `/home/user/create_backup.py` and run it to archive the contents of `/home/user/source_data/` into a backup directory `/home/user/backup_dir/`.

Here are the strict requirements for the archiver:

1. **Target Files & Traversal**: 
   The script must accept two arguments: an input directory and an output file path. It must recursively traverse the input directory. Only files ending with the `.log` or `.txt` extensions should be included in the archive. All other files (e.g., `.json`, `.bak`) must be ignored.

2. **Custom "Compression" Step**:
   For every file included, you must read its byte contents, completely **reverse the order of the bytes**, and then compress the reversed bytes using Python's standard `zlib.compress()` function.

3. **Archive Format**:
   The output file must be a binary file adhering exactly to this custom format:
   - **Header**: The first 8 bytes must be the ASCII string `CUST_ARC`.
   - **File Entries**: For each included file (sorted alphabetically by their relative path to ensure deterministic output), append the following:
     - The length of the relative file path as an unsigned short (2 bytes, little-endian). The relative path should not start with a slash (e.g., `app/sys.log`).
     - The relative file path encoded in UTF-8.
     - The size of the compressed payload as an unsigned int (4 bytes, little-endian).
     - The compressed byte payload.

4. **Atomic Write Management**:
   To ensure a backup is never partially written if the script crashes, the archive must first be constructed and written entirely to a temporary file in the same output directory. Once the temporary file is completely written and closed, it must be atomically renamed to the final output path. 
   To prove this was done, your script must append a log entry to `/home/user/backup_operation.log` with the exact line: 
   `Atomically renamed <TEMP_FILE_PATH> to <FINAL_FILE_PATH>`

**Execution Phase**:
Once you have written `/home/user/create_backup.py`, execute it to archive `/home/user/source_data/` into the destination `/home/user/backup_dir/final_backup.carc`. 

*Note: You must create `/home/user/backup_dir/` if it does not exist.*