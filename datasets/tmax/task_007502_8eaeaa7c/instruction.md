You are a backup administrator. You need to safely archive log files from a live system that are actively being written to. 

Write a C program at `/home/user/archive_tool.c` that performs the following operations:
1. Searches the directory `/home/user/data/` for files ending in `.log`.
2. Filters these files based on metadata: only process `.log` files that are strictly greater than 50 bytes in size.
3. The logs are currently encoded in `ISO-8859-1`. For each valid file found, your C program must:
   a. Open the file and acquire a shared file lock using `flock()` to prevent reading partial records while concurrent writers are active.
   b. Read the file contents and convert them from `ISO-8859-1` to `UTF-8` in memory (you may use the `iconv` API).
   c. Release the file lock and close the file.
   d. Append the converted UTF-8 text to a single archive file located at `/home/user/safe_backup.txt`.
   
For each processed file, append exactly this format to `/home/user/safe_backup.txt`:
```
--- [filename] ---
[UTF-8 content]
```
Where `[filename]` is just the base name of the file (e.g., `app_error.log`), not the full path.

Compile your program and run it so that `/home/user/safe_backup.txt` is generated successfully.