You are a performance engineer tasked with profiling a scientific computing application. The application performs Markov Chain Monte Carlo (MCMC) sampling and Singular Value Decomposition (SVD) to estimate a posterior distribution.

A colleague has written the application in Python, located at `/home/user/mcmc_svd_target.py`. It takes a single positional argument: an integer random seed. It outputs the wall-clock execution time (in seconds) to standard output.

We need to statistically validate the average runtime of this script to ensure it meets our performance SLAs. Due to system restrictions on the profiling server, you must implement the profiling and statistical analysis using **Bash** and standard UNIX utilities (like `awk`, `sed`, `grep`, `bc`, etc.). You may not use Python or R to perform the statistical analysis.

Your task:
1. Write a Bash script at `/home/user/profile.sh` that executes `/home/user/mcmc_svd_target.py` 30 times, using seeds 1 through 30 (inclusive).
2. Save the runtime output of each run to `/home/user/runtimes.txt` (one runtime per line, 30 lines total).
3. Within the same `/home/user/profile.sh` script, implement a non-parametric Bootstrap algorithm using `awk` (or `bash`/`bc`) to calculate the 95% confidence interval for the mean runtime. 
    - You must perform exactly 10,000 bootstrap resamples.
    - Calculate the mean of each resample.
    - Find the 2.5th percentile and 97.5th percentile of these 10,000 means to form the 95% CI.
4. Output the final confidence interval to `/home/user/ci_output.txt` in the exact format: `lower_bound,upper_bound` (e.g., `1.452,1.512`). Round to 3 decimal places.

Ensure `/home/user/profile.sh` is executable and runs the entire pipeline (data collection + bootstrap analysis) when invoked without arguments.