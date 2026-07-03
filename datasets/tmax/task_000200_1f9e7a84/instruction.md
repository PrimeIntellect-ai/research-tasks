You are investigating an issue in a long-running data-processing service written in Bash. 

The service is located at `/home/user/service.sh`. It processes a continuous stream of numeric data from `/home/user/stream.txt`. 

Users have reported two major issues:
1. **Memory Leak**: The service's memory usage grows unbounded over time until the OOM killer terminates it.
2. **Numerical Instability**: The variance it calculates starts returning `0` or highly inaccurate results after the data values shift into a higher numeric range. The script currently uses the naive variance formula ($E[X^2] - E[X]^2$), which is suffering from catastrophic cancellation.

Your task:
1. Debug and identify the root causes of the memory leak and the math instability.
2. Write a corrected version of the script to `/home/user/fixed_service.sh`. The fixed script must:
   - Compute the rolling **population variance** for a window size of 10.
   - Use a numerically stable two-pass approach (calculate the mean of the window first, then the average of the squared deviations from the mean).
   - Prevent the memory usage from growing continuously (do not store unbounded historical data).
   - Maintain the same output format (print the variance for each window to stdout).
3. Run your fixed script on `/home/user/stream.txt` and save ONLY the final calculated variance (the last line of output) to `/home/user/final_variance.txt`.

Ensure your fixed script is executable and utilizes basic shell utilities (like `awk`) appropriately for the math, but avoids the cancellation issue.