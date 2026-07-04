You are a localization engineer managing a telemetry pipeline for translation strings. Your system receives logs in JSON-Lines format containing usage data for localized strings.

A previous engineer wrote a C tool (`/home/user/l10n/parse_logs.c`) to parse these logs and extract the `timestamp`, `locale`, and `message`. However, the tool is buggy: it crashes (Segmentation fault) whenever it encounters a Unicode escape sequence (e.g., `\uXXXX`) in the `message` field because of out-of-bounds memory access in its naive string traversal. 

Your tasks are:

1. **Fix the C Parser**: Modify `/home/user/l10n/parse_logs.c` so that it correctly handles `\uXXXX` sequences (you can simply replace the 6-character sequence `\uXXXX` with a placeholder `?` to prevent crashes, or decode it properly). The program must read `/home/user/l10n/input.jsonl` from standard input and output a Tab-Separated Values (TSV) format to standard output: `timestamp\tlocale\tmessage`.
   - Compile it to `/home/user/l10n/parse_logs`.

2. **Resampling and Gap-Filling**: Write a bash script `/home/user/l10n/process.sh` that pipes `/home/user/l10n/input.jsonl` through your fixed C program. Using shell utilities (`awk`, `sort`, etc.) within the script, aggregate the data to count the total number of logs *per hour* (using integer division of the epoch timestamp by 3600). 
   - You must output a continuous time-series CSV to `/home/user/l10n/hourly_counts.csv` with the format `hour_timestamp,count`. 
   - **Crucial**: You must fill in any "gaps" (missing hours between the minimum and maximum hour in the dataset) with a count of `0`.

3. **Stratified Sampling**: In the same `/home/user/l10n/process.sh` script, generate a stratified sample of the parsed logs. Extract exactly the *first* (chronologically earliest) log entry for *each* unique locale found in the parsed TSV. 
   - Save this to `/home/user/l10n/stratified_sample.tsv` (format: `timestamp\tlocale\tmessage`).

4. **Pipeline Scheduling**: Install a cron job for the `user` that runs `/home/user/l10n/process.sh` at the top of every hour (i.e., minute 0). 

Ensure all files are correctly placed in `/home/user/l10n/`.