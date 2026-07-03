You are an AI assistant helping a backup administrator archive and analyze backup logs. We have a directory containing backup logs at `/home/user/backup_data`. Unfortunately, a misconfigured script has created circular symbolic links within this directory, which causes our standard shell scripts to enter infinite loops. Furthermore, the log files can be quite large, and entries often span multiple lines.

Your task is to write a robust log parser in C, compile it, and then process its output using standard Linux text processing tools (`awk`, `sed`, etc.).

Step 1: Write a C program `/home/user/parse_logs.c` and compile it to `/home/user/parse_logs`.
The program must:
1. Recursively traverse the directory passed as its first argument (e.g., `/home/user/backup_data`).
2. Safely detect and SKIP symbolic links to avoid infinite loops. For every symbolic link encountered, print exactly: `SYMLINK: <full_path_to_symlink>\n` to `stdout`.
3. For regular files, use memory-mapped I/O (`mmap`) to read the file contents efficiently.
4. Parse the file as a multi-line log. Every distinct log entry begins with a timestamp on a new line in the format `[YYYY-MM-DD]`. An entry continues until the next timestamp or the end of the file.
5. If a multi-line entry contains the exact string `CRITICAL_FAILURE` (anywhere in the entry), print the *entire* entry to `stdout`, prefixed with the absolute file path and a colon. 
   Format of the output for a matching entry:
   ```
   <absolute_file_path>: [YYYY-MM-DD] <rest of the first line>
   <line 2 of entry>
   <line 3 of entry>
   ```
   *(Note: Ensure there is exactly one space after the colon following the file path. Do not add extra newlines between entries).*

Step 2: Run your C program
Run `/home/user/parse_logs /home/user/backup_data > /home/user/raw_critical.txt`.

Step 3: Create a summary using text transformation tools
Using tools like `awk`, `sed`, or `grep` on `/home/user/raw_critical.txt`, generate a CSV file at `/home/user/summary.csv`.
The CSV should contain only the entries that had a `CRITICAL_FAILURE`. It must have the following format (no header row):
`<absolute_file_path>,<YYYY-MM-DD>`

For example, if `/home/user/raw_critical.txt` contains:
```
SYMLINK: /home/user/backup_data/loop_dir/link_back
/home/user/backup_data/server1.log: [2023-10-12] Backup initiated
System unresponsive...
CRITICAL_FAILURE detected on device /dev/sda1
Aborting.
```
Your `/home/user/summary.csv` must contain:
`/home/user/backup_data/server1.log,2023-10-12`

Ensure that your C code handles the recursive directory traversal and memory mapping correctly. Do not use external libraries for the C program other than standard POSIX C libraries (`<stdio.h>`, `<stdlib.h>`, `<fcntl.h>`, `<sys/mman.h>`, `<sys/stat.h>`, `<dirent.h>`, `<string.h>`, `<unistd.h>`).