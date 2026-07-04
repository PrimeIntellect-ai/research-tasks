You are acting as a backup administrator archiving system data. We have a set of legacy binary backup files scattered across several directories. To catalog these properly before moving them to cold storage, you need to extract specific metadata headers from these binary files based on an index. 

Your task is to write and execute a C program that automates this extraction process. 

Here are the requirements:

1. **Input Data**:
   - There is an index file located at `/home/user/backups/index.csv`.
   - The CSV has a header row and follows the format: `BackupID,RelativePath,HeaderOffset`
   - The `RelativePath` is relative to the `/home/user/backups/` directory.
   - `HeaderOffset` is the integer byte offset within the binary file where the backup metadata header begins.

2. **Binary Header Format**:
   - At the specified offset in each binary file, there is a 16-byte header.
   - Bytes 0-3: A 4-byte magic number.
   - Bytes 4-7: A 32-bit unsigned integer (little-endian) representing a Unix timestamp.
   - Bytes 8-15: Reserved (ignore these).

3. **What You Need to Do**:
   - Write a C program at `/home/user/archive_tool.c`.
   - The program must open and parse `/home/user/backups/index.csv`.
   - For each entry in the CSV, open the corresponding binary file, navigate to the specified `HeaderOffset`, and read the header.
   - Extract the magic number as an uppercase hexadecimal string (e.g., "DEADBEEF").
   - Extract the timestamp as an integer.
   - Write the extracted information into a JSON array in a file located at `/home/user/archive_summary.json`.

4. **Output Format**:
   The output file `/home/user/archive_summary.json` must be a valid JSON array of objects, exactly formatted (spacing/newlines don't matter as long as it's valid JSON) with the keys `BackupID`, `Magic`, and `Timestamp`. Example:
   ```json
   [
     {
       "BackupID": "BK001",
       "Magic": "BADF000D",
       "Timestamp": 1672531200
     },
     {
       "BackupID": "BK002",
       "Magic": "DEADBEEF",
       "Timestamp": 1672617600
     }
   ]
   ```

5. **Execution**:
   - Compile your C program using standard `gcc`.
   - Run the program to generate the `/home/user/archive_summary.json` file.
   - You may use standard C libraries. You can construct the JSON string manually in C using `fprintf`, as the structure is very simple.

Ensure your C program is robust enough to handle the paths properly and compiles successfully.