You are a storage administrator responsible for managing disk space on a logging server. The directory `/home/user/logs` contains various `.log` files spread across multiple subdirectories. To free up space, you need to identify specific log files that have been marked for archiving, compress them into a secure archive, and prepare a report.

Your task consists of the following steps:

1. Write a C program named `/home/user/filter_logs.c`. 
   - The program must read absolute file paths from standard input (stdin), one per line.
   - For each file path, it must open the file and use `mmap` (memory-mapped I/O) to efficiently scan the file's contents.
   - It should search for the exact string "ARCHIVE_ME" anywhere in the file.
   - If the file contains the string, the program must print the file path to standard output (stdout), followed by a newline.
   - Ensure the program handles errors gracefully (e.g., if a file cannot be opened or mapped, it should simply skip it).

2. Compile your C program to the executable `/home/user/filter_logs`.

3. Using standard bash commands (like `find`), search the `/home/user/logs` directory for all files with the `.log` extension. Pipe this list of files into your `/home/user/filter_logs` executable, and redirect the output to `/home/user/archived_list.txt`. This file will serve as your report.

4. Create a gzipped tar archive named `/home/user/cold_storage.tar.gz` that contains exactly the files listed in `/home/user/archived_list.txt`. Ensure that you do not include files that are not in the list.

5. Verify the integrity of the created archive `/home/user/cold_storage.tar.gz` using standard archive tools (e.g., `tar -tzf` or `gzip -t`) to ensure it is not corrupt.

Ensure that all file paths in `/home/user/archived_list.txt` are absolute paths.