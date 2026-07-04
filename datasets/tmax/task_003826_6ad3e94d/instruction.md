You are acting as a performance engineer who needs to process some server profiling data.

I wrote a Bash script located at `/home/user/aggregate.sh` to parse our profiling metrics from `/home/user/metrics.csv`. The script is supposed to clean the data (capping CPU usage at 100.0 if it reads 99.9 due to a known sensor artifact) and then calculate the average CPU and Memory usage. 

However, I'm running into two major issues:
1. The script completely hangs and never finishes when running on the current `metrics.csv`. It seems to be stuck in an infinite loop.
2. Previously, when it ran on a dataset without the sensor artifact, it lost all decimal precision in the final averages, just spitting out whole numbers.

Your task is to debug and modify `/home/user/aggregate.sh` to fix these issues. 
Requirements:
- Fix the loop termination issue so the script completes.
- Correct the formula and precision loss: both the `AvgCPU` and `AvgMem` calculated at the end must retain exactly 3 decimal places (e.g., `12.345`). Use `bc` correctly to achieve this.
- Make sure the 99.9 -> 100.0 capping logic actually applies to the running total.
- Execute the fixed script so that it outputs the final averages to `/home/user/results.txt`.

The output file `/home/user/results.txt` must have exactly this format:
AvgCPU: [value]
AvgMem: [value]