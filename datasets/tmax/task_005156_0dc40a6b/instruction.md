You are a log analyst investigating patterns in a legacy system. You have received a noisy log file located at `/home/user/raw_logs.txt`. 

Your task is to write a C++ program to process, clean, deduplicate, and resample these logs, and write the output to `/home/user/processed_logs.txt`.

The raw log file has the following format for each line:
`YYYY-MM-DD HH:MM:SS | USER_ID | MESSAGE`

Here are the exact processing rules your C++ program must implement:

1. **Cleaning**: The `MESSAGE` field contains encoding errors and noise. You must clean the message by removing any character that is NOT a printable ASCII character (keep only characters with decimal ASCII values from 32 to 126 inclusive).
2. **Global Deduplication**: Some logs are repeated. If a combination of `USER_ID` and the *cleaned* `MESSAGE` has been seen in any earlier line of the file, discard the current line. (Use a hash set or similar structure to keep track of seen combinations).
3. **Resampling and Gap-Filling**: The output must have exactly one log entry per minute, spanning from `2023-10-01 10:00:00` to `2023-10-01 10:15:00` inclusive (exactly 16 entries).
   - For each minute bin, select the valid (not discarded by deduplication) log entry that occurred *earliest* within that minute.
   - If a minute bin has no valid entries, you must fill the gap by generating a synthetic log entry with `USER_ID` as `SYSTEM` and `MESSAGE` as `NO_ACTIVITY`.
4. **Output Format**: Write the resampled results to `/home/user/processed_logs.txt`. The timestamps in the output must be rounded down to the minute (i.e., seconds must be `00`).
   Format: `YYYY-MM-DD HH:MM:00 | USER_ID | CLEANED_MESSAGE`

Compile and run your C++ program to generate the `/home/user/processed_logs.txt` file. Make sure your C++ code is robust and handles the strict time boundaries.