You are a DevOps engineer doing forensic analysis on a log processing pipeline. A legacy log ingester written in C, located at `/home/user/log_processor`, is failing intermittently and crashing with a Segmentation Fault when processing the daily log dump located at `/home/user/app_logs.txt`. 

The log file contains exactly 10,000 log entries. One of the log entries is corrupted and triggers a vulnerability in the parser, but because the tool does not print intermediate state cleanly, it's unclear which line is causing the crash.

Your tasks are to:
1. Use delta debugging / bisection techniques on the input file `app_logs.txt` to identify the exact line number (1-indexed) of the corrupted log entry causing the crash.
2. Analyze the source code provided in `/home/user/log_processor.c` and use intermediate state tracing (e.g., GDB or printf debugging) to identify why the corrupted input causes a segmentation fault.
3. Fix the vulnerability in `/home/user/log_processor.c` so that it safely ignores the corrupted line (skipping the processing for that line without crashing) and continues processing the rest of the file.
4. Recompile the tool (using `gcc /home/user/log_processor.c -o /home/user/log_processor`).
5. Run the fixed binary on the entire `/home/user/app_logs.txt` file. When the tool successfully reaches the end of the file, it will print a final status string formatted as `SUCCESS_TOKEN: <alphanumeric_string>`.

Once you have completed these steps, create a file at `/home/user/solution.txt` containing exactly two lines in the following format:
```
Crashing Line: <line_number>
Token: <alphanumeric_string>
```

Replace `<line_number>` with the 1-indexed line number of the corrupted log entry, and `<alphanumeric_string>` with the token printed by the repaired C program.