I need you to write a C++ program to help organize and parse a messy project data directory. The data is located at `/home/user/project_data/` and contains a mix of binary files (`*.dat`) and multi-line log files (`*.log`). Unfortunately, a faulty backup script previously created some symbolic links in this directory that loop back on themselves, creating infinite recursion if traversed naively.

Your C++ program must do the following:

1. **Recursive Traversal with Loop Detection**: Recursively traverse `/home/user/project_data/`. You must handle symbolic links but prevent infinite loops (e.g., by tracking visited device/inode pairs or absolute paths).

2. **Binary Header Extraction and Atomic Writes**: 
   For every `.dat` file found:
   - The file starts with a 9-byte header: 
     - Signature: 4 bytes `DAT\x00`
     - Version: 1 byte (unsigned char)
     - Data Length: 4 bytes (unsigned int, little-endian)
   - Following the header is the actual data payload of size `Data Length`.
   - You must read the payload and save it to `/home/user/processed/dat/<original_filename>`.
   - To prevent data corruption during processing, you must use **atomic writes**: write the payload to a temporary file in `/home/user/processed/dat/` first, and then rename it to the final filename.

3. **Multi-line Log Record Parsing**:
   For every `.log` file found:
   - The file contains records that start with the line `[RECORD_START]` and end with the line `[RECORD_END]`. Records can span multiple lines.
   - You must extract any complete record (excluding the `[RECORD_START]` and `[RECORD_END]` marker lines themselves) that contains the exact substring `[CRITICAL]` anywhere inside it.
   - Append all extracted critical records to a single file at `/home/user/processed/critical_errors.txt`. Separate each extracted record with a blank line. Do not include records from the same log file multiple times if they are evaluated per file.

**Constraints & Execution**:
- You must write the solution in C++ (e.g., `parser.cpp`) and compile it with `g++ -std=c++17 parser.cpp -o parser`.
- Create the output directories `/home/user/processed/dat/` before writing to them.
- Run the compiled `parser` executable to process the files.
- Ensure all resources are properly managed and no infinite symlink loops trap your program.