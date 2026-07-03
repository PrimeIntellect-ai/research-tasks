You are tasked with helping a developer organize a messy legacy project repository. 

There is a directory at `/home/user/raw_data/` containing numerous binary files (`*.bin`) scattered across deep subdirectories. Some of these files are valid telemetry data files, while others are corrupted or unrelated binaries.

You need to write a C program and a bash script to parse, filter, and organize these files.

**Step 1: Write a C parser (`/home/user/parser.c`)**
Write a C program that takes a file path as a command-line argument. The program MUST use memory-mapped I/O (`mmap`) to read the file. 
The valid telemetry binary files have the following exact structure (Little Endian):
- Offset 0: 4 bytes (uint32_t) - Magic Number: `0xC0DEFEED`
- Offset 4: 4 bytes (uint32_t) - Unix Epoch Timestamp
- Offset 8: 16 bytes (char array) - Project Code string (null-terminated)
- Offset 24: 8 bytes (double) - Metric Value

If the file does not have the magic number `0xC0DEFEED` at the beginning, or if the file is smaller than 32 bytes, the program should exit with code 1 and output nothing.
If the file is valid, the program should extract the timestamp, project code, and metric value, and print them to standard output in the following pipe-separated format:
`TIMESTAMP|PROJECT_CODE|METRIC`
(Print the metric value with exactly 4 decimal places).

**Step 2: Organize the Files**
Write a script (e.g., `/home/user/organize.sh`) that does the following:
1. Searches for all `.bin` files inside `/home/user/raw_data/`.
2. Uses your compiled C program to inspect each file.
3. If the file is a valid telemetry file, move it to a new directory structure under `/home/user/organized_project/`.
   The destination path must be: `/home/user/organized_project/<PROJECT_CODE>/<YYYY-MM>/<original_filename>`
   (Where YYYY-MM is the year and month derived from the Unix timestamp, in UTC).
4. For every valid file processed, append a JSON record to `/home/user/parsed_metrics.jsonl`. The JSON must be strictly on a single line per file (JSON Lines format) and contain these keys:
   `{"file": "<original_filename>", "timestamp": <unix_timestamp>, "project": "<PROJECT_CODE>", "metric": <metric_value>}`

Ensure your scripts create any missing directories as needed. 
Do not leave any valid `.bin` files in the `raw_data` directory. Invalid `.bin` files should be left exactly where they are.