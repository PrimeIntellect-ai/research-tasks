You are an AI assistant helping a backup administrator archive a mix of manufacturing and system data. The data is located in `/home/user/backup_source`. 

Your task is to write a C++17 program (e.g., `archiver.cpp`) that automates the cleanup, preparation, and formatting of these files before they are pushed to cold storage. You must compile and run this program to process the files.

The `/home/user/backup_source` directory contains a nested structure with various files. Your C++ program must recursively traverse this directory and perform the following actions based on the file type:

1. **GCode Files (files ending in `.gcode`):**
   * **Encoding Conversion:** The files are currently encoded in ISO-8859-1. You must convert their contents to UTF-8.
   * **Parsing/Cleaning:** Strip out all comments. A comment begins with a semicolon (`;`) and continues to the end of the line. Also, remove any empty lines that result from this process (or that already existed).
   * **Chunking:** Split the cleaned UTF-8 content into chunk files of exactly 100 bytes each (the final chunk may be smaller). Name the chunks `<original_filename>.part001`, `<original_filename>.part002`, etc. (1-based padding to 3 digits), placed in the exact same directory as the original file.
   * **Cleanup:** Delete the original `.gcode` file after it has been successfully chunked.

2. **ELF Binaries:**
   * **Detection:** Check the first 4 bytes (magic number) of all files. If a file begins with `\x7F ELF` (`7F 45 4C 46`), it is an ELF binary. (Ignore files that have already been renamed to `.elf.bak`).
   * **Renaming:** Rename these ELF files by appending `.elf.bak` to their current filename.

3. **Manifest Generation:**
   * Write a log file to `/home/user/manifest.log`.
   * For every ELF file renamed, write a line: `RENAMED ELF: <relative_path_from_backup_source_to_new_file>`
   * For every GCode chunk created, write a line: `CHUNKED GCODE: <relative_path_from_backup_source_to_chunk_file>`
   * Output lines in the manifest should be sorted alphabetically.

**Requirements:**
- Use C++17 or higher.
- You may use any standard library headers.
- Build your code using `g++ -std=c++17 -O2 archiver.cpp -o archiver`.
- Execute your binary. 
- You do not need to process files that do not match the above criteria.