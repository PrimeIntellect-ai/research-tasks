You are a performance engineer tasked with profiling a custom C-based Monte Carlo simulation.

Your environment contains a C source file at `/home/user/mc_sim.c`. This program performs a Monte Carlo estimation of Pi and measures its own CPU execution time. It accepts a single command-line argument: the number of iterations ($N$).

Your task consists of three phases:

**Phase 1: Compilation**
Compile `/home/user/mc_sim.c` into an executable named `/home/user/mc_sim`. You must use `gcc` with the `-O3` optimization flag.

**Phase 2: Execution and Profiling**
Write a bash script or use a loop in the terminal to run `/home/user/mc_sim` exactly 50 times with $N = 50000000$ (50 million). 
Capture the standard output of each run (which is the execution time in seconds as a float) and append it to `/home/user/times.txt`. Each line in `/home/user/times.txt` should contain exactly one float.

**Phase 3: Bootstrap Confidence Intervals**
Write and execute a Python script at `/home/user/bootstrap.py` that reads the execution times from `/home/user/times.txt` and calculates a 95% bootstrap confidence interval for the *mean* execution time.
Your Python script MUST adhere to the following strict requirements for reproducibility:
- Read the values from `/home/user/times.txt` into a numpy array of floats.
- Set the numpy random seed: `numpy.random.seed(42)`
- Perform exactly $B = 10000$ bootstrap resamples. In each iteration, use `numpy.random.choice(times, size=len(times), replace=True)` to generate a bootstrap sample, and compute its mean.
- Calculate the 2.5th and 97.5th percentiles of the bootstrap means using `numpy.percentile(bootstrap_means, [2.5, 97.5])`.
- Save the resulting lower and upper bounds to a file named `/home/user/bootstrap_ci.txt` in the exact format: `lower_bound,upper_bound` (e.g., `0.1234,0.1456`), rounded to 6 decimal places.

Ensure all output files are placed exactly at the specified absolute paths.