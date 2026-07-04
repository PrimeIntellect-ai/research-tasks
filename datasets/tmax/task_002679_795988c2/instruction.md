You are tasked with building a C program for a configuration management system that tracks file size changes across internationally distributed servers. 

The configuration update logs are stored in different formats depending on the region, and they contain server names with various Unicode characters. You must write a C program that parses these multi-format files, calculates rolling statistics on the changed bytes, and properly counts the length of the UTF-8 server names.

**Task Requirements:**

1. **Input Data**:
   The input files are located in `/home/user/configs/`. You will find two files:
   * `/home/user/configs/eu.csv` (Comma-separated values: `server_name,timestamp,bytes_changed`)
   * `/home/user/configs/asia.tsv` (Tab-separated values: `server_name\ttimestamp\tbytes_changed`)

2. **C Program Specifications**:
   * Create your C program at `/home/user/config_tracker.c` and compile it to an executable named `/home/user/config_tracker`.
   * The program should accept multiple file paths as command-line arguments (e.g., `./config_tracker /home/user/configs/eu.csv /home/user/configs/asia.tsv`).
   * It must determine the file format dynamically based on the file extension (`.csv` parses with `,` delimiter, `.tsv` parses with `\t` delimiter).
   * For every record processed (in the exact order the files and lines are read), compute a **rolling moving average** of the `bytes_changed` for that specific `server_name`. The rolling window size is **3**. (i.e., the average of the last up to 3 records for that server).
   * Calculate the true number of characters (Unicode code points) in the `server_name` string, accounting for UTF-8 multi-byte sequences.

3. **Output format**:
   * Output the results sequentially to a file at `/home/user/output.txt`.
   * For each line in the input files, append a line to the output in the exact following format:
     `{server_name} ({char_count} chars): {bytes_changed} bytes, avg: {rolling_avg}`
   * `rolling_avg` must be formatted as a floating-point number with exactly 2 decimal places.

**Example output line:**
`srv-東京 (6 chars): 300 bytes, avg: 250.00`

Ensure your program handles missing or malformed lines gracefully (if any), though you can assume the provided files generally follow the specified structure. Do not use external C libraries outside of the standard POSIX C library (e.g., `<stdio.h>`, `<stdlib.h>`, `<string.h>`).