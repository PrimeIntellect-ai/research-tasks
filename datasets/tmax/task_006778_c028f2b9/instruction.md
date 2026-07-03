You are helping a developer organize and parse a scattered collection of custom-compressed log files across a project repository. 

There is a directory located at `/home/user/project_logs` which contains a deep, nested directory structure. Scattered throughout these directories are several log files with the `.clog` extension.

These `.clog` files use a custom Run-Length Encoding (RLE) compression format. You need to write a C program (save it as `/home/user/log_parser.c`) to traverse the directory structure, decompress these files, parse the multi-line log records, and extract specific error records.

**File Format Specification (.clog):**
- The file contains no headers.
- It is comprised entirely of 2-byte pairs: `[count][character]`.
- `count` is a 1-byte unsigned integer (`uint8_t`) representing the number of times the character is repeated (from 1 to 255).
- `character` is a 1-byte ASCII character (`uint8_t`).
- For example, the pair `0x04 0x41` decompresses to `AAAA`.

**Log Record Specification (Decompressed):**
- Once decompressed, the file contains plain text log records.
- Each log record begins with a timestamp and log level in the format: `[YYYY-MM-DD HH:MM:SS] LEVEL: `
- Valid levels are `INFO`, `WARN`, `ERROR`, and `DEBUG`.
- A log record may span multiple lines (e.g., stack traces). A record continues until the next `[` character at the start of a line, or until the end of the file.

**Your Objective:**
1. Write a C program `/home/user/log_parser.c` and compile it.
2. The program must recursively traverse `/home/user/project_logs` to find all `.clog` files.
3. For each `.clog` file, it should use memory-mapped I/O (`mmap`) or efficient streaming to read and decompress the file in memory.
4. Extract all multi-line log records where the level is `ERROR`.
5. Write the extracted `ERROR` records to `/home/user/error_summary.log`.

**Output Format for `/home/user/error_summary.log`:**
For each error found, append to the file using the following exact format:
```
---
File: <relative path to .clog file from /home/user/project_logs>
<the exact decompressed multi-line error log record>
```
*Note: The relative path should NOT start with a slash. e.g., `backend/db.clog`. Include the trailing newline of the log record.*

Sort the output by the relative file path alphabetically. If a file has multiple errors, they should appear in the order they were found in the file.

Execute your program to create `/home/user/error_summary.log`. You are done when the file is correctly generated.