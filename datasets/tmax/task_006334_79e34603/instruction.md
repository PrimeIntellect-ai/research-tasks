You are an AI assistant acting as a storage administrator. We are experiencing recurring disk space issues caused by a runaway logging process. A massive log file has been generated at `/home/user/system.log`.

Your objective is to extract specific disk space error blocks from this large log file, scrub sensitive session data from these blocks, and create a backup archive of the extracted data. You must write a C++ program to perform the heavy lifting of parsing and scrubbing.

Here are your specific instructions:

1. **C++ Extractor Program**:
   - Write a C++ program at `/home/user/extractor.cpp`.
   - The program must open and read `/home/user/system.log` efficiently (assume the file could be larger than available RAM, so process it line-by-line or in chunks).
   - Log lines start with a timestamp prefix like `[YYYY-MM-DD HH:MM:SS]`.
   - You need to find all multi-line log events that begin with a line containing the exact string `ERROR: Disk Space Critical`.
   - An event block starts with this `ERROR` line and includes all subsequent lines until (but excluding) the very next line that begins with a `[` character (which denotes the start of the next log event).
   - For each matching error block found, you must scrub any sensitive session tokens. Specifically, replace any occurrence of `SESSION_TOKEN=[a-zA-Z0-9]+` with `SESSION_TOKEN=REDACTED`.
   - Save each extracted, scrubbed block into a separate file in the directory `/home/user/disk_errors/`.
   - Name the files sequentially: `error_1.log`, `error_2.log`, `error_3.log`, etc., based on the order they appear in `system.log`.

2. **Execution**:
   - Compile your program to `/home/user/extractor`. Use `g++` with standard C++17.
   - Run the program to generate the files in `/home/user/disk_errors/`. Ensure the directory is created if it does not exist.

3. **Backup Archive**:
   - Once the files are extracted, use standard Linux shell commands to create a compressed gzip tarball of the `/home/user/disk_errors/` directory.
   - Save the archive exactly at `/home/user/errors_backup.tar.gz`.

Ensure all paths and file names match exactly as specified. Do not remove the original `/home/user/system.log`.