You are a log analyst investigating patterns in a custom server application. You have been provided with a log file at `/home/user/server_logs.txt`. 

Your task is to write a C program that parses this file, extracts error codes using regular expressions, calculates summary statistics, and generates monitoring logs.

Requirements:
1. Write a C program at `/home/user/analyzer.c`.
2. The program must accept two command-line arguments: the input log file path, and the output CSV file path. Example: `./analyzer /home/user/server_logs.txt /home/user/stats.csv`
3. The program must read the input file line by line.
4. Use standard POSIX regular expressions (`<regex.h>`) to identify lines that contain either `[ERROR]` or `[FATAL]`.
5. For lines that match, extract the 3-digit error code that appears immediately after the string `ErrorCode: ` (e.g., if the line contains `ErrorCode: 404`, extract `404`).
6. Aggregate these extracted codes to count how many times each specific error code appears among the `[ERROR]` and `[FATAL]` logs.
7. Write these summary statistics to the specified output CSV file. The CSV must have a header `ErrorCode,Count`, followed by the aggregated data sorted in ascending order by the ErrorCode.
8. Implement pipeline monitoring: Before exiting, your C program must append exactly one line to `/home/user/monitor.log` in the exact format: `Processed X lines. Found Y critical errors.` (where X is the total number of lines read from the log file, and Y is the total number of `[ERROR]` and `[FATAL]` lines found).

Compile your code using `gcc -o /home/user/analyzer /home/user/analyzer.c` and run it against the provided `/home/user/server_logs.txt` to generate `/home/user/stats.csv` and `/home/user/monitor.log`.