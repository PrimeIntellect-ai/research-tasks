You are a performance engineer tasked with profiling a scientific computing routine and setting up a regression test for its convergence. 

We have a Monte Carlo simulation script located at `/home/user/mc_pi.py` that estimates the value of Pi. However, we need to formally profile its execution time, test its convergence properties, and implement a bash-based regression check.

Please perform the following steps:

1. Write a Python profiling script at `/home/user/profile_mc.py`. This script must:
   - Import `math`, `time`, `random`, and the `estimate_pi` function from `mc_pi.py`.
   - Set the random seed exactly once at the very beginning of the execution using `random.seed(42)`.
   - Loop over the following sample sizes: `N = [1000, 10000, 100000, 1000000]`.
   - For each `N`, measure the wall-clock execution time of `estimate_pi(N)` using `time.time()`.
   - Calculate the absolute error of the estimation compared to `math.pi`.
   - Write the results to a CSV file at `/home/user/mc_results.csv`. The file should contain exactly 4 lines (no headers), with each line formatted as: `N,execution_time,absolute_error`.

2. Execute your Python script to generate `/home/user/mc_results.csv`.

3. Write a bash shell script at `/home/user/verify.sh` that acts as a simple scientific regression test:
   - It should read `/home/user/mc_results.csv`.
   - Extract the absolute error for `N=1000` (first line) and `N=1000000` (fourth line).
   - Compare the two floating-point errors. If the error for `N=1000000` is strictly less than the error for `N=1000`, the script must print exactly `Convergence OK` to standard output and exit with status code 0.
   - If it is not strictly less, print `Convergence FAIL` and exit with status code 1.
   - Make sure `/home/user/verify.sh` is executable.

You do not need to modify `/home/user/mc_pi.py`. Just write the profiling script, generate the data, and create the verification bash script.