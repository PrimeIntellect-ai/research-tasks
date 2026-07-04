You are an incident response analyst investigating an ongoing issue. You have been provided with a raw log file at `/home/user/input_logs.txt`. 

The log file has the following space-separated format:
`[TIMESTAMP] IP_ADDRESS ERROR_CODE MESSAGE`

To identify patterns without getting overwhelmed by noise, you need to create a custom log processor.

Write a C++ program and save it to `/home/user/stratified_dedup.cpp`. The program must read logs from standard input line by line and apply the following logic:
1. **Constraint-based Validation:** Discard any log where the `ERROR_CODE` is not a numeric value between `400` and `599` (inclusive).
2. **Hash-based Deduplication:** For valid logs, track the uniqueness of the `(ERROR_CODE, MESSAGE)` combination. Duplicate combinations should be ignored.
3. **Stratified Sampling:** Output only the first 2 unique log entries encountered for each `ERROR_CODE`. Once an `ERROR_CODE` has 2 unique messages recorded, completely ignore any further logs with that `ERROR_CODE`.

Compile your program to `/home/user/stratified_dedup`.

Finally, run your compiled program on `/home/user/input_logs.txt`, sort the output numerically by the `ERROR_CODE` (3rd column) ascending, and then alphabetically by the `MESSAGE` (4th column) ascending. Save the final sorted output to `/home/user/investigation_results.txt`.

Ensure your C++ code is efficient and strictly adheres to the filtering limits. Do not hardcode the log entries in your C++ code.