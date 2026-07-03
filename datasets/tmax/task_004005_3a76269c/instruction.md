You are a performance engineer tasked with debugging a critical mathematical script. 

We have a Python script located at `/home/user/calc_variance.py`. This script is designed to compute the sample variance of a large dataset iteratively, calculating a "rolling variance" as it processes the file `/home/user/data.txt`.

Currently, the application suffers from three major issues:
1. **Application Crash:** The script fails to complete and crashes with an error before producing the final result. You must analyze the traceback/logs and fix the logic flaw (there is a boundary/off-by-one condition in the array indexing).
2. **Performance Bottleneck:** Even before it crashes, the script is running agonizingly slow. Use system call tracing or profiling to identify why it's so slow and fix the bottleneck. The script should run in under a second.
3. **Precision Loss:** The mathematical formula used to calculate the rolling variance suffers from catastrophic cancellation (precision loss) because the numbers in `data.txt` are very large (around 1,000,000) but their differences are small. You must replace the naive variance formula with a numerically stable algorithm (like Welford's method) or correctly use a multi-pass approach to ensure the final calculated variance is mathematically accurate.

Your objective:
1. Debug and modify `/home/user/calc_variance.py` to fix the crash, resolve the catastrophic cancellation, and eliminate the I/O performance bottleneck.
2. Run the fixed script so that it successfully completes and writes the final accurate variance to `/home/user/result.txt` (format to 6 decimal places).
3. Ensure `/home/user/progress.log` correctly logs the progress, but without causing a massive system call bottleneck (e.g., open the file once and write to it, or buffer the writes, rather than opening/closing it on every single iteration).

Do not change the input dataset `/home/user/data.txt`. 
You can install any standard debugging tools (like `strace`) if you need them.