You are tasked with handling a security and parsing issue for our custom configuration manager. We receive configuration updates packaged in a custom binary archive format called `.cpk` (ConfigPack). Recently, we suspect that malicious actors are trying to use path traversal ("Zip Slip") attacks within these archives to overwrite sensitive system files outside the intended extraction directory.

Your objective is to write a C program that parses the `.cpk` archive, extracts legitimate files, blocks malicious ones, and then process the logs into a summary report.

**Archive Format Specification (`.cpk`):**
1. **Magic Bytes**: The file must start with exactly 4 bytes: `CPK1`.
2. **File Count**: An unsigned 32-bit integer (little-endian) representing the number of files in the archive.
3. **File Entries** (repeated sequentially):
   - **Filename Length**: An unsigned 16-bit integer (little-endian) representing the length of the filename.
   - **Filename**: A string of bytes of the specified length (NOT null-terminated in the file).
   - **File Size**: An unsigned 32-bit integer (little-endian) representing the size of the file data.
   - **File Data**: The raw bytes of the file.

**Requirements:**
1. Write a C program at `/home/user/parser.c`. Compile it to `/home/user/parser`.
2. The program must read `/home/user/update.cpk`.
3. Check the magic bytes. If they are not `CPK1`, the program should print an error and exit with status `1`.
4. Create the directory `/home/user/extracted/` (if it doesn't exist) and any required subdirectories for valid files.
5. Iterate through the files in the archive:
   - **Path Traversal Check**: If the filename contains the substring `../` or starts with a `/`, it is considered malicious.
   - **Malicious Files**: Do NOT extract them. Instead, append a line to `/home/user/malicious.log` exactly in this format:
     `[THREAT] <filename> : <size>`
   - **Legitimate Files**: Extract them into `/home/user/extracted/`. For example, a safe file `configs/app.conf` should be written to `/home/user/extracted/configs/app.conf`. 
6. Run your compiled C program.
7. After execution, use a text transformation tool (`awk`, `sed`, etc.) to parse `/home/user/malicious.log` and generate a CSV report at `/home/user/threat_report.csv`. The CSV should have the exact format:
   `<filename>,<size>`
   (Do not include a header row, and strip the `[THREAT] ` prefix and spaces around the `:`).

Ensure all extracted files have exactly the bytes specified in the archive, and the threat report is formatted perfectly.