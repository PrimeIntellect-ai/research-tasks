I need your help to organize a messy directory of project files and prepare them for uploading to a storage server. The files are located in `/home/user/build_dump`.

The directory contains a mix of compiled binaries, corrupted files, and large text logs. I need you to write and execute a Bash script that performs the following organization tasks:

1. **ELF Binary Filtering and Archiving**:
   - Analyze all files in `/home/user/build_dump`.
   - Identify all *valid, 64-bit ELF executables*. Beware: there are some corrupted files that might have an ELF extension or start with the ELF magic bytes but are completely invalid and cannot be parsed by standard tools like `readelf`.
   - Copy the valid 64-bit ELF executables into a new directory: `/home/user/elf_valid`. Keep their original filenames.
   - Create a gzip-compressed tarball named `/home/user/elf_archive.tar.gz` containing the contents of `/home/user/elf_valid/` (just the files, do not include the `elf_valid` directory structure in the archive).

2. **Log File Splitting and Archiving**:
   - Find all files ending with `.log` in `/home/user/build_dump`.
   - Create a directory `/home/user/log_chunks`.
   - Split each `.log` file into 50 Kilobyte (50 * 1024 bytes) chunks. 
   - The chunks must be saved in `/home/user/log_chunks/` and named using the format `<original_filename>_chunk_aa`, `<original_filename>_chunk_ab`, etc. (Use the default alphabetic suffixes of the standard `split` command).
   - Once all logs are split, create a ZIP archive named `/home/user/logs_archive.zip` containing all the chunk files in `/home/user/log_chunks/` (again, just the files, not the directory structure).

3. **Summary Verification**:
   - After completing the above operations, create a summary text file at `/home/user/summary.txt` containing exactly two lines in the following format:
     ```
     VALID_ELF_COUNT=<number_of_valid_elfs>
     LOG_CHUNK_COUNT=<total_number_of_log_chunks>
     ```
     *(Replace `<...>` with the actual integer counts).*

Please execute the necessary commands to accomplish this. You can create temporary scripts if needed. Ensure all final archives and directories are placed exactly at the paths specified.