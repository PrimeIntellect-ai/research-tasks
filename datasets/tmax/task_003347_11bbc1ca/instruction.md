You are an engineer tasked with investigating and fixing a critical issue in a Python statistics service. 

We have a script located at `/home/user/stats_service.py` that processes a large dataset to calculate the sample variance of a stream of numbers. However, the service currently has two major problems:
1. **Memory Leak**: The service crashes with an Out-Of-Memory (OOM) error when processing very large streams because it retains all data points in memory.
2. **Floating-Point Precision**: The current mathematical formulation for variance suffers from catastrophic cancellation (loss of significance) when dealing with values that have large magnitudes but small differences. This leads to wildly inaccurate or even negative variances.

Your task:
1. Comprehend the existing code in `/home/user/stats_service.py`.
2. Rewrite the `StatsTracker` class to compute the sample variance in a strictly online, single-pass manner without storing the history of data points. This will fix the memory leak.
3. Use a numerically stable algorithm (e.g., Welford's online algorithm) to fix the floating-point precision issue.
4. The entry point of the script (`main`) reads from `/home/user/data.txt` and writes the final variance to `/home/user/output.txt`. Do not change the file paths or the output format in `main()`.

To verify your solution, ensure that your updated `stats_service.py` can correctly process a generated dataset without storing elements in a list, and outputs the exact variance to `/home/user/output.txt`. Once you are confident in your fix, run the script against the provided `/home/user/data.txt` and leave the corrected code and `output.txt` on the disk.