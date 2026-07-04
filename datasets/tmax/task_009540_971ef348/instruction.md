I need your help organizing a messy directory of project files located at `/home/user/project_dump`. The directory contains a deep, nested hierarchy of files, many of which have incorrect or missing extensions. 

I need a bash script at `/home/user/organize.sh` that will recursively traverse `/home/user/project_dump` and do the following:

1. **Identify 64-bit ELF binaries:** Detect them by reading the first 5 bytes of the file. A 64-bit ELF file always starts with the magic bytes `7F 45 4C 46 02` (in hex), which represents `\x7fELF` followed by `\x02` (Class 64).
2. **Identify WAL (Write-Ahead Log) files:** Detect them by reading their first 7 bytes. Valid WAL files in our project start with the exact byte sequence `WAL_v3\x00` (where `\x00` is a null byte).
3. **Safely Organize Them:** 
   - Create two target directories: `/home/user/organized/elf64/` and `/home/user/organized/wal/`.
   - Copy the identified files into their respective directories. 
   - To avoid collisions and standardize names, the destination filename must be the SHA-256 hash of the file's contents (e.g., `/home/user/organized/elf64/e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
   - **Important:** Because another process might be reading the destination directories, you must ensure atomic file creation in the destination directories. To do this, copy the file to a temporary name (e.g., appending `.tmp` to the hash name) in the destination directory first, and then rename (`mv`) it to the final hash-based filename.
4. **Create an Inventory Log:** Create a file at `/home/user/inventory.txt` that lists all successfully copied files. Each line must be exactly in this format:
   `<original_absolute_path> -> <final_absolute_path>`

Please write and execute the script. Do not process files that do not match the exact binary headers mentioned above.