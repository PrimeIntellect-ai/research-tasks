You are an engineer investigating false alerts in a long-running service monitor. A Bash script `/home/user/calc_variance.sh` processes memory usage logs (`/home/user/mem_stats.log`) to compute the rolling population variance of memory consumed. 

Because the baseline memory usage is high (around 1,000,000,000 bytes) and standard `awk` uses double-precision floats, the naive variance formula `(sumsq / n) - (sum / n)^2` suffers from catastrophic cancellation and precision loss. Over time, this formula implementation error causes the script to output mathematically impossible negative variance values.

Your objectives:
1. **Precision Loss Tracking:** Execute the original `/home/user/calc_variance.sh` on `/home/user/mem_stats.log`. Identify the exact line number (which corresponds to the record `n`) where the calculated variance *first* becomes strictly less than 0. Write ONLY this line number to `/home/user/failure_line.txt`.
2. **Formula Implementation Correction:** Create a corrected script `/home/user/fixed_calc_variance.sh` that calculates the rolling population variance without precision loss by implementing Welford's online algorithm in `awk`. 
    - The script must take the log file path as its first argument.
    - It must output `n var` for each line, identical to the original script's intended behavior.
    - Do not use any external tools other than standard `awk` inside the Bash script (e.g., do not use `bc`, Python, or Perl).
    - Ensure it is executable.

The final system state will be verified by checking `/home/user/failure_line.txt` and running `/home/user/fixed_calc_variance.sh` on a hidden test file.