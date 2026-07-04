You are a backup administrator archiving critical system logs. 

You have been given two log files: `/home/user/log_v1.txt` (the previous backup) and `/home/user/log_v2.txt` (the current state). The current log file contains everything in the previous log, plus several new appended lines.

Your task is to perform an incremental backup and custom compression of specific high-priority log entries:

1. **Incremental Extraction & Transformation**: Extract ONLY the newly added lines in `/home/user/log_v2.txt` (the incremental difference). Using text transformation tools (like `sed`, `awk`, or `grep`), filter these new lines to keep only those containing the exact string `[ARCHIVE_ME]`. Save these filtered lines to `/home/user/to_archive.txt`.

2. **Custom Compression with C**: Write a C program at `/home/user/mmap_compress.c` that reads `/home/user/to_archive.txt` entirely using `mmap()` (memory-mapped I/O) for efficient streaming.
   
3. **Compression Algorithm**: The C program must apply a custom Run-Length Encoding (RLE) to the mapped memory. For any sequence of consecutive identical characters (including spaces, symbols, and newlines) of length `N >= 4`, replace the sequence with `*N<char>`, where `N` is the integer count of the character, and `<char>` is the character itself. For sequences shorter than 4, leave the characters exactly as they are. 
   - *Example 1*: `aaaaa` becomes `*5a`
   - *Example 2*: `error    code` (4 spaces) becomes `error*4 code`
   - *Example 3*: `***` remains `***`
   - *Example 4*: `..........` becomes `*10.`

4. **Output**: The C program must write the compressed text to `/home/user/archive.z`.

Compile and run your C program to produce the final `/home/user/archive.z` file.