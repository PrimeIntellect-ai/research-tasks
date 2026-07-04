As a backup administrator, you have been tasked with archiving executable binaries from a chaotic legacy application tree. The directory structure is known to contain symlinks that form infinite loops, which routinely crash naive backup scripts. 

Your objective is to write a robust C program that navigates the directory structure, identifies true ELF binaries, and archives them safely.

Create your C program at `/home/user/archiver.c` and compile it to `/home/user/archiver`.

The program must meet the following requirements:
1. **CLI Arguments:** Accept exactly three arguments: `./archiver <source_directory> <destination_directory> <log_file_path>`
2. **Safe Navigation:** Recursively traverse `<source_directory>`. You **MUST** follow symlinks to directories, but you **MUST NOT** fall into infinite loops. You will need to track visited directories (e.g., by device and inode numbers) to prevent infinite recursion.
3. **Format Parsing:** For every regular file encountered (after resolving symlinks), read its first 4 bytes. Process the file ONLY if it is a valid ELF executable (magic bytes: `0x7F`, `'E'`, `'L'`, `'F'`). Skip all other file types and non-ELF files.
4. **Copy and Bulk Rename:** Copy every discovered ELF file into the flat `<destination_directory>`. The copied file must be renamed using the format: `<original_filename>_<original_inode>.bak`. (Use the inode of the resolved regular file).
5. **Streaming Log:** Append a record to `<log_file_path>` for every successfully copied file in the exact format:
   `COPIED: <absolute_path_of_original_resolved_file> -> <absolute_path_of_destination_file>`
   *(Note: Ensure paths in the log are absolute. You can use `realpath` for the original file path).*

Create the `/home/user/backup_dir` directory and run your program to archive `/home/user/app_tree` into `/home/user/backup_dir`, writing the log to `/home/user/backup_log.txt`.

You are expected to write, compile, and execute the C code to accomplish this task.