You are acting as a storage administrator managing disk space and data ingestion for an old logging system. We have received a batch of legacy backup archives that need to be processed, but there are several issues. The archives are heavily nested, contain a custom binary log format, and our security team has warned us that the archiving system had a bug which occasionally included absolute paths or directory traversal payloads (Tar Slip) which could overwrite critical system files.

Your task is to safely extract, rename, convert, and store these logs. 

Here are the detailed steps and requirements:

1. **Archive Handling and Safety:**
   - The master archive is located at `/home/user/backups/master_backup.tar.gz`.
   - Inside it are multiple inner `.tar` files, which in turn contain `.blog` (Binary Log) files.
   - You must safely extract all `.blog` files into `/home/user/extracted_logs/`.
   - **CRITICAL:** You must ensure that no files are extracted outside of `/home/user/extracted_logs/`. Some archives may contain malicious paths (e.g., `../` or absolute paths aiming for `/home/user/system_state.json`). Do not let `system_state.json` get overwritten!

2. **Bulk Renaming:**
   - As you extract them, flatten the directory structure so all `.blog` files are directly in `/home/user/extracted_logs/`.
   - Rename them sequentially to match the pattern: `log_0001.blog`, `log_0002.blog`, etc., sorted alphabetically by their original base filename.

3. **Format Conversion (C Programming):**
   - Write a C program at `/home/user/convert_logs.c` to convert the `.blog` files into `.csv` format. Compile it to `/home/user/convert_logs`.
   - **Binary Format (`.blog`):**
     - Header: 4 bytes magic number `0x424C4F47` (ASCII 'BLOG').
     - Records (repeated until EOF):
       - Timestamp: 4 bytes, unsigned 32-bit integer, little-endian.
       - Event ID: 2 bytes, unsigned 16-bit integer, little-endian.
       - Severity: 1 byte, unsigned 8-bit integer.
       - Payload Length: 1 byte, unsigned 8-bit integer.
       - Payload: variable length string of characters (length specified by Payload Length). It is NOT null-terminated in the file.
   - **Output Format (`.csv`):**
     - CSV Header: `Timestamp,EventID,Severity,Payload`
     - Each record should be printed on a new line.

4. **Atomic Writes:**
   - The C program must use **atomic writes** to prevent partial file corruption if the disk fills up. 
   - Specifically, your C program must write the CSV data to a temporary file (e.g., ending in `.tmp`), ensure the data is flushed to disk, and then use the POSIX `rename()` function to atomically move it to the final `.csv` filename.
   - Run your compiled C program on all the renamed `.blog` files.
   - Save the final `.csv` files in `/home/user/processed_logs/` with the same base name (e.g., `log_0001.csv`).

Verify your work by ensuring `/home/user/processed_logs/` contains the cleanly converted CSVs, and that `/home/user/system_state.json` remains unaltered.