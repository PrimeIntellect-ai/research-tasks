You are acting as an AI assistant for a performance engineer. I need you to help me debug and fix a performance profiling pipeline that has recently started reporting incorrect latency averages. 

Here is the situation:
We extract raw memory states from our servers to analyze execution times. Recently, our aggregation script started giving slightly inaccurate moving averages and dropping records, which broke our performance dashboards.

Please perform the following steps:

1. **Memory Dump Analysis:**
   Extract the raw performance metrics from the simulated memory dump located at `/home/user/app_memory.dump`. The metrics are embedded within binary data as printable ASCII strings in the exact format: `PERF_RECORD: <timestamp> <duration_ms>`. 
   Extract only these valid lines (preserving their order) and save them to `/home/user/extracted_records.txt`. Remove the "PERF_RECORD: " prefix so that the file contains only `<timestamp> <duration_ms>` on each line.

2. **Git Bisection:**
   The aggregation script is located in a Git repository at `/home/user/perf_tools`. The script is named `analyze_profile.sh`. We know the script worked correctly 10 commits ago (the commit tagged as `v1.0`), but the current `HEAD` is broken. 
   Find the exact commit hash that introduced the bug and save the full 40-character commit hash to `/home/user/bad_commit.txt`. 

3. **Debugging and Repair:**
   Fix the `analyze_profile.sh` script in the `master` branch. The script has introduced regressions involving:
   - **Floating-point precision / Formula correction:** The script calculates the average latency but is failing to maintain floating-point precision, likely due to a recent change from `bc`/`awk` to native bash arithmetic or poor precision handling. Ensure the final average is correctly calculated as a float.
   - **Boundary condition:** The script drops the very last record of the dataset due to a misguided attempt to remove trailing blank lines using an off-by-one loop or `head/tail` logic.
   - **Timezone/Offset Bug:** The script filters out records before a given `START_TIME`. However, a recent commit added a hardcoded 3600-second (1 hour) timezone offset subtraction to the filter condition incorrectly, skipping valid records. Remove this timezone offset error so timestamps are compared raw.

4. **Execution:**
   Run your fixed `analyze_profile.sh` script using `/home/user/extracted_records.txt` as the input file and `1700000000` as the `START_TIME`.
   Usage: `./analyze_profile.sh /home/user/extracted_records.txt 1700000000 > /home/user/final_report.txt`

The script should output to `final_report.txt` in the following format:
`Processed: <count> records`
`Average Latency: <average> ms` (The average MUST be rounded to exactly 3 decimal places).

Make sure all your fixes are applied and the final report is generated.