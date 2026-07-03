You are a support engineer investigating a critical failure in a custom C-based data processing pipeline. The program, `log_processor`, is designed to parse CSV log files and calculate average request durations. Recently, it has started crashing with a Segmentation Fault when processing the daily logs.

Your task is to perform a root-cause analysis by finding the regression, analyzing the crash, and identifying the anomalous data. 

Here is your environment:
- Repository: `/home/user/log_engine`
- The `main` branch is currently crashing. 
- A known good tag is `v1.0`.
- The problematic data file: `/home/user/data/server_logs.csv`

Perform the following steps:
1. **Git Bisection:** Use `git bisect` (or manual binary search) to identify the exact commit hash that introduced the crashing behavior. You can compile the code at any commit by running `gcc -g -o log_processor processor.c`. The program is run as `./log_processor <path_to_csv>`.
2. **Stack Trace Analysis:** Compile the code at the *bad commit* with debug symbols (`-g`). Run it under `gdb` to capture the backtrace when the segmentation fault occurs. Identify the exact C function name and the line number in `processor.c` where the crash happens.
3. **Data Anomaly Investigation:** Inspect `/home/user/data/server_logs.csv` to find the specific anomalous line that triggers the crash (the parsing logic fails on a specific structural anomaly). Identify the line number (1-indexed) in the CSV.

Finally, write your findings into a diagnostic report at `/home/user/diagnostic_report.txt` using EXACTLY the following format:

```
Bad Commit: <full_40_character_git_hash>
Segfault Function: <exact_function_name>
Segfault Line: <integer_line_number>
Anomalous Data Line: <integer_csv_line_number>
```

Ensure the file contains only these four lines. Do not include any extra text.