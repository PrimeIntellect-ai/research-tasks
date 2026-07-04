You are tasked with analyzing a series of daily configuration dumps to find an anomaly in our system's resource scaling. 

Our configuration management system saves daily snapshots of server settings in the `/home/user/configs/` directory. Each file is named in the format `config_YYYY-MM-DD.txt`. 

Inside these files, configurations are stored as space-separated key-value pairs, one per line. We are specifically interested in tracking the `MAX_CONNECTIONS` key. However, the configuration system is messy:
- The key might be written in uppercase, lowercase, or mixed case (e.g., `MAX_CONNECTIONS`, `max_connections`, `Max_Connections`).
- The values are sometimes written in standard base-10 decimal (e.g., `100`), and sometimes in base-16 hexadecimal (e.g., `0x64`).

Your objectives are:
1. Write a C program at `/home/user/analyzer.c` that takes one or more file paths as command-line arguments. For each file, it must:
   - Extract the date from the filename.
   - Tokenize and parse the file to extract the value associated with the `MAX_CONNECTIONS` key (case-insensitive).
   - Normalize the extracted value into a standard base-10 integer.
   - Print the result to standard output in the format: `YYYY-MM-DD <base-10-value>` (one per line).

2. Compile your C program to `/home/user/analyzer`.

3. Use your compiled program and standard Linux shell commands to process all the text files in `/home/user/configs/` in chronological order. 

4. Perform changepoint detection to identify the **first date** where the `MAX_CONNECTIONS` value increased by **strictly more than 50%** compared to the chronologically preceding day's value. 

5. Save *only* that specific date (in `YYYY-MM-DD` format) to the file `/home/user/anomaly.txt`.