You are an IT support technician handling an escalated ticket regarding a containerized overnight financial batch processing job. 

The developer writes:
"Our aggregation container intermittently crashes with a `ValueError: math domain error`. I managed to pull the logs from the last failed run and saved them to `/home/user/container_logs.txt`. The crash seems to happen when calculating standard deviations of transaction amounts. Even when it doesn't crash, we've noticed the standard deviation values are sometimes suspiciously off (likely due to floating-point precision loss). The script is located at `/home/user/aggregate_transactions.py` and the data it processes is in the `/home/user/transactions/` directory."

Your task:
1. Inspect the logs and the script to understand the precision loss and the intermittent crash.
2. Fix the `/home/user/aggregate_transactions.py` script so that it calculates the standard deviation in a numerically stable way (avoiding catastrophic cancellation and negative variances). You may use Python's built-in libraries to solve the precision issue.
3. Run the fixed script against the `/home/user/transactions/` directory.
4. Save the corrected output to `/home/user/fixed_results.txt`. The output must have exactly one line per batch file in the format: `filename,standard_deviation_rounded_to_4_decimals` (e.g., `batch_1.csv,1.4142`).

Do not change the command line arguments the script accepts, just fix its internal calculation and write the final results.