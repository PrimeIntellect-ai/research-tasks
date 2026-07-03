You are a backup administrator recovering data from a partially corrupted backup storage drive. 

The directory `/home/user/backup_drive/` contains a scattered set of backup fragments. Unfortunately, an old backup script created infinite symlink loops within this directory structure (e.g., directories linking back to their parents). 

Your task is to safely navigate this directory, extract the backup data, and parse it.

Here are your instructions:
1. Safely locate all file fragments ending with the `.frag` extension inside `/home/user/backup_drive/` without falling into the infinite symlink loops.
2. Merge these fragments together in alphabetical order of their filenames (e.g., `chunk_A.frag`, then `chunk_B.frag`) to create a single merged file at `/home/user/merged.bin`.
3. The merged file is a custom binary log format. Write a C program at `/home/user/parser.c` to parse `/home/user/merged.bin`. 
4. The binary format consists of a sequence of records. Each record has:
   - A 4-byte unsigned integer (little-endian) representing the length of the log entry (`L`).
   - Exactly `L` bytes of ASCII text (the log entry), which may span multiple lines.
5. Your C program should read the binary file, extract all the ASCII log entries, and print them to standard output.
6. Compile and run your program. Filter the output to find ONLY the complete multi-line log entries that contain the word "CRITICAL". Note that a log entry might be several lines long; if "CRITICAL" appears anywhere in the entry, the *entire* multi-line entry must be outputted.
7. Save the resulting multi-line CRITICAL log entries to `/home/user/critical_logs.txt`. Separate each distinct matching log entry with a single line containing exactly `---`.

Ensure your C program handles the binary data correctly and that you don't get trapped by the symlinks during your search!