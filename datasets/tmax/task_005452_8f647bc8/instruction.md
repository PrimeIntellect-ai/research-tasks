You are a DevOps engineer analyzing application access logs to calculate billing metrics based on bandwidth and processing time. 

You have been provided with a buggy Python script located at `/home/user/calculate_billing.py` and a CSV log file at `/home/user/app_logs.csv`. 

Currently, the script fails with a traceback when it encounters corrupted input data in the logs. Even when the corrupt lines are manually removed, the calculated output does not match the expected billing formula due to a logical error in the code.

Your task is to debug and fix `/home/user/calculate_billing.py` to meet the following requirements:

1. **Corrupted Input Handling**: 
   - The script must read `/home/user/app_logs.csv` and process the data.
   - If a line contains invalid `bytes` or `duration` values (e.g., cannot be parsed as a float, or is empty), catch the exception, skip the line, and continue processing.
   - Write the 1-based line numbers (where the header is line 1) of all skipped corrupted lines to a log file at `/home/user/corrupt_lines.log`, with one line number per line.

2. **Formula Correction**:
   - The billing formula should calculate the cost per row as: 
     `Cost = (bytes in Megabytes) * 0.02 + (duration) * 0.005`
   - Note: 1 Megabyte (MB) = 1,048,576 bytes.
   - The original script incorrectly multiplies raw bytes without converting them to Megabytes first. You must correct this.

3. **Output Generation**:
   - Aggregate the total cost per `user_id`.
   - Output the final totals as a JSON dictionary to `/home/user/billing_summary.json`. The keys should be the `user_id` and the values should be the total cost rounded to 4 decimal places.

Fix the script and run it to produce the correct `/home/user/corrupt_lines.log` and `/home/user/billing_summary.json`. You can test your script by executing `python3 /home/user/calculate_billing.py`.