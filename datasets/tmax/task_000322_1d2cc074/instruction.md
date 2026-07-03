You are a log analyst investigating server performance patterns. You have been given a raw, noisy log file at `/home/user/raw_logs.txt`.

Your task is to write a C program that cleans the logs, aligns timestamps, deduplicates entries, and calculates a rolling average of request durations.

Requirements:
1. Write your C program to `/home/user/process_logs.c` and compile it to `/home/user/process_logs`.
2. The program must read from `/home/user/raw_logs.txt` and write its output to `/home/user/rolling_stats.csv`.
3. **Cleaning:** Ignore any lines that do not match the exact format `[YYYY-MM-DD HH:MM:SS.mmm] INFO duration=<integer>`. (Note the square brackets and the space between the timestamp and INFO).
4. **Timestamp Alignment & Deduplication:** Truncate the timestamp to the nearest second (i.e., drop the `.mmm` milliseconds part). If multiple valid log entries occur within the *exact same second*, keep **only the first** valid entry encountered for that second and ignore the rest.
5. **Rolling Statistics:** For each kept entry, compute the rolling average of the `duration` using a sequence-based window of the last 3 kept entries (including the current one). 
   - For the 1st kept entry, the average is just its duration.
   - For the 2nd kept entry, the average is the sum of the 1st and 2nd divided by 2.
   - For the 3rd and subsequent entries, the average is the sum of the last 3 divided by 3.
6. **Output Format:** The output file `/home/user/rolling_stats.csv` must contain the aligned timestamp and the rolling average formatted to exactly 2 decimal places, separated by a comma. 
   Example line: `2023-10-12 10:00:00,100.00`

Execute your compiled C program so that `/home/user/rolling_stats.csv` is generated successfully.