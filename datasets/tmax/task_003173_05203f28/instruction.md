You are a performance engineer profiling a new microservice. The service's task execution times have been recorded and saved as raw binary data. Theoretical models suggest these execution times follow an Exponential distribution.

Your task is to estimate the distribution parameter, validate the empirical variance against the analytical expected variance, and log the results.

1. You will find a binary file at `/home/user/execution_times.bin` containing exactly 1,000,000 `double` (64-bit IEEE 754 floating-point) values representing execution times in seconds.
2. Write a C program at `/home/user/profiler_stats.c` that:
   - Reads the binary file.
   - Fits the data to an Exponential distribution by calculating the Maximum Likelihood Estimate (MLE) for the rate parameter $\lambda$ (Lambda). (Hint: For an exponential distribution, $\lambda = 1 / \text{mean}$).
   - Calculates the empirical sample variance of the data.
   - Calculates the analytical variance of the fitted Exponential distribution based on your estimated $\lambda$ (Hint: Analytical Variance = $1 / \lambda^2$).
3. Compile your C program from source into an executable named `/home/user/profiler_stats` (use `gcc`).
4. Run your program and have it generate a plain text log file at `/home/user/stats_output.txt` with exactly the following three lines (replace the brackets with your calculated floating-point values formatted to exactly 5 decimal places):
   ```
   Estimated Lambda: [value]
   Empirical Variance: [value]
   Analytical Variance: [value]
   ```

Make sure your C program reads the binary data correctly and computes the sample variance using the standard unbiased estimator (divide by N-1).