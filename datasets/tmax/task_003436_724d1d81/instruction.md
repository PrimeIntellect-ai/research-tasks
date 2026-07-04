You are tasked with recovering and organizing a developer's project files from a proprietary backup system. The backup daemon records incremental file changes (creations, modifications, deletions) into a custom Write-Ahead Log (WAL) binary format. 

You must write a robust Python script at `/home/user/parse_backup.py` to parse this WAL file and compute the final, up-to-date state of the project directory.

However, the documentation for the proprietary WAL format was lost. The only surviving reference is a photo of the developer's whiteboard located at `/app/whiteboard.png`. You will need to extract the binary format specification from this image (you can use `pytesseract` or similar tools).

Your script must meet the following requirements:
1. **Invocation**: It must run via `python3 /home/user/parse_backup.py <path_to_wal_file>`.
2. **File Locking**: The backup daemon might still be running. Before reading the file, your script must open it and acquire a shared lock (`fcntl.LOCK_SH`) on the WAL file descriptor to prevent concurrent writes during parsing. Release the lock after reading.
3. **Parsing**: Parse the binary WAL file according to the schema found in `/app/whiteboard.png`. 
4. **State Resolution**: Track the incremental changes to compute the final state. 
    - `CREATE` or `UPDATE` operations set or overwrite the file's state with a new checksum.
    - `DELETE` operations remove the file from the current state.
5. **Output**: Once parsed, print the final directory state to standard output. Sort the active files alphabetically by their full path. The output format must be exactly:
    `<path> : <8-character zero-padded hex checksum>`
    (e.g., `src/main.py : 00a1b2c3`)

Do not print anything else to standard output besides the final sorted state. Ensure your script handles edge cases gracefully, such as deleting a file that doesn't exist (ignore the deletion) or updating a file that wasn't created (treat as create).