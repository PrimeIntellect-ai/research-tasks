You have just inherited an unfamiliar codebase for a log processing system. The system uses a Bash script to merge and sort log files from various regional servers. However, the script is currently producing incorrect and corrupted results.

Your task is to debug and fix the script located at `/home/user/log_processor/process_logs.sh`. 

The script is supposed to:
1. Read all `.log` files in the `/home/user/log_processor/logs/` directory.
2. Extract the timestamp (first two space-separated fields) and the message.
3. Convert the timestamp to a Unix epoch for accurate sorting.
4. Sort all log entries by epoch time and save the result to `out/final.log`.

However, there are several critical bugs you must identify and resolve:
1. **Corrupted Input Handling:** The input log files occasionally contain binary null bytes (`\x00`) due to a known logging agent bug. These must be cleanly stripped out before processing the lines.
2. **Race Condition:** The script uses background jobs to process files concurrently to save time, but it writes to a shared temporary file `out/tmp.log` without locking, resulting in interleaved lines and dropped messages. You must fix this concurrency bug (e.g., by using separate temporary files per job and combining them, or safely synchronizing writes).
3. **Timezone Bug:** The logs contain naive timestamps (e.g., `2023-10-01 12:00:00`). The script assumes they are in the local system timezone. However, the timezone is implied by the file name:
   - Files named `us-east_*.log` are in `America/New_York` timezone.
   - Files named `eu-west_*.log` are in `Europe/London` timezone.
   - Files named `asia_*.log` are in `Asia/Tokyo` timezone.
   You must modify the script to parse the timezone from the filename prefix and set the `TZ` environment variable appropriately for the `date` command so that the epoch conversion is accurate.
4. **Regression Test:** Create a bash script at `/home/user/log_processor/test.sh` that tests your fixed `process_logs.sh`. It should create mock input files covering the null byte issue, the race condition (sufficient volume), and timezone differences, run the script, and verify that the final output is perfectly sorted and contains no data loss. It must exit with `0` on success and `1` on failure.

Save your corrected script to `/home/user/log_processor/process_logs_fixed.sh` and ensure it writes its final sorted output to `/home/user/log_processor/out/final.log`. 

Finally, execute your fixed script against the provided logs and copy the resulting `out/final.log` to `/home/user/log_processor/verification.log`.