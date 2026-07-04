You are acting as a backup administrator who needs to archive a set of multi-line transaction logs into a highly compact, custom binary format.

Your task is to write a C program that recursively traverses a specific directory, parses multi-line text logs, converts the data into a binary structure, and saves it to an archive file. 

Here are the requirements:

1. **Input Data**: 
   - Directory to traverse: `/home/user/log_backups`
   - Look for all files with the `.txt` extension.
   - The files contain multi-line records. Each record starts with `---START---` and ends with `---END---`.
   - Between these markers, the record has the following format:
     ```
     Time: <Unix Epoch Timestamp (integer)>
     Severity: <INFO | WARN | CRIT>
     Message: <Any text, which might span multiple lines>
     ```
   
2. **Output Format**:
   - Write the parsed records into a binary file at `/home/user/archive.bin`.
   - **Header**: The first 4 bytes of the file must be the ASCII string `BKP1`.
   - **Records**: After the header, write each record using the following exact binary layout (little-endian for integers):
     - Timestamp: 8-byte unsigned integer (`uint64_t`)
     - Severity: 1-byte unsigned integer (`uint8_t`) where INFO = 0, WARN = 1, CRIT = 2.
     - Message Length: 2-byte unsigned integer (`uint16_t`) representing the length of the message text (excluding any null terminator).
     - Message: The literal bytes of the message text. Do NOT include a null terminator in the file. Strip leading/trailing whitespaces from the message before calculating its length and writing it.
   
3. **Sorting Constraint**:
   - The records in the `archive.bin` file must be sorted chronologically by the Timestamp in ascending order. If two records have the same timestamp, preserve their relative order as discovered.

Write the C code (save it as `/home/user/archiver.c`), compile it, and run it to produce `/home/user/archive.bin`.