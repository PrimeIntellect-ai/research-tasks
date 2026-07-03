You are a backup administrator tasked with archiving a massive legacy log file. The log contains mixed critical and non-critical data, and some of the text needs character normalization before it can be safely stored in the new archive system.

Your task consists of the following steps:

1. **Parse Configuration:** 
   There is a configuration file located at `/home/user/archive_config.txt`. It contains various settings, including the target destination directory specified in the format `ARCHIVE_DEST = /path/to/dir # inline comment`. 
   Using shell tools like `sed` or `awk`, parse this file to extract the exact directory path (ignoring any whitespace and comments). Create this destination directory if it does not already exist.

2. **Develop an Archiving Tool in C:**
   Write a C program at `/home/user/archiver.c` that takes exactly two command-line arguments: an input file path and an output file path.
   The program must:
   - Open and read the input file exclusively using memory-mapped I/O (`mmap`). 
   - Scan the memory-mapped data line by line.
   - Extract only the lines that begin with the exact prefix `[KEEP] `.
   - Perform character conversion on these extracted lines: convert all lowercase alphabetical characters (`a-z`) to uppercase (`A-Z`).
   - Write the transformed lines to the specified output file using standard buffered I/O (e.g., `fwrite`, `fprintf`, or `fputs`).

3. **Execute the Pipeline:**
   - Compile your C program to an executable named `/home/user/archiver` (e.g., using `gcc`).
   - Run the archiver. Pass `/home/user/raw_backup.log` as the input file, and have it write the output to a file named `processed_data.txt` inside the destination directory you extracted in Step 1.

4. **Generate Verification Log:**
   Create a log file at `/home/user/summary.log` containing exactly one line with the total number of lines successfully written to `processed_data.txt`. (Format: `Total archived: X` where X is the number of lines).