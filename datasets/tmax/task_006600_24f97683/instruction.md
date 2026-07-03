You are a system reliability engineer investigating a custom long-running metrics aggregation service written in Bash. The service, located at `/home/user/metrics_service`, is currently failing to start properly, crashing on edge-case data, calculating incorrect statistics, and has been reported to consume unbound memory over time (a memory leak in Bash).

Your objective is to debug and fix the script `/home/user/metrics_service/metricsd.sh` and its associated components. 

Here are the specific issues reported:
1. **Startup Compilation Error**: The bash script attempts to compile a small C helper (`/home/user/metrics_service/fast_stat.c`) on startup to do heavy lifting, but the compilation fails with a linker error.
2. **Floating-point Precision Loss**: The bash script calculates a "stability score" using `bc` for specific metrics, but the output is always an integer (e.g., `0`) instead of the correct precise decimal value (it should be calculated to exactly 4 decimal places).
3. **Format Parsing Edge-case**: The service tails a CSV file. However, if a line has trailing whitespace before the newline, or an empty field, the script's `IFS=, read` logic misaligns the variables, causing invalid data to be passed to the helper. You must fix the parsing logic to gracefully handle and strip trailing whitespaces and ignore completely blank lines.
4. **Memory Leak**: The script keeps a historical record of all processed transaction IDs in a global Bash array (`processed_tx_ids`) to check for duplicates. As the service runs forever, this array grows indefinitely, causing the bash process to consume gigabytes of RAM. Modify the logic so it only keeps a rolling window of the last 100 transaction IDs in the array, preventing unbounded memory growth while retaining duplicate-checking for recent items.

Instructions:
1. Inspect the code in `/home/user/metrics_service/`.
2. Fix the C compiler/linker error in `metricsd.sh`.
3. Fix the `bc` floating-point precision bug in `metricsd.sh`.
4. Fix the format parsing edge case in `metricsd.sh`.
5. Fix the array memory leak in `metricsd.sh`.
6. Once you are confident in your fixes, run the validation script: `/home/user/metrics_service/test_service.sh`. 
7. If your fixes are correct, the test script will write a validation code to `/home/user/metrics_service/status.log`.