You are a data scientist working on a machine learning simulation project. Recently, our C++ extension for vector reductions was updated to use a new multi-threaded parallel sum. Because floating-point addition is not strictly associative, the order of reductions is now non-deterministic, causing the final model metrics to vary slightly across runs even with a fixed random seed.

We need to implement a scientific code regression test to ensure these floating-point variations don't represent a statistically significant drift from our baseline. 

I have placed the following files in your home directory (`/home/user`):
1. `simulate.py`: A Python wrapper around the simulation that prints a single floating-point metric to standard output.
2. `baseline_mean.txt`: Contains a single float, the exact mean of the metric from 10,000 runs on the old, strictly sequential version of the code.
3. `bootstrap_ci.R`: An R script that takes a file of floats (one per line) as its first argument and prints the 95% bootstrap confidence interval of the mean as two space-separated floats: `[LOWER] [UPPER]`.

Your task is to orchestrate this regression test using bash. Write a shell script at `/home/user/run_regression.sh` that does the following:
1. Executes `python3 /home/user/simulate.py` exactly 50 times, appending each output to a new file called `/home/user/current_runs.txt`.
2. Uses `Rscript /home/user/bootstrap_ci.R /home/user/current_runs.txt` to calculate the 95% bootstrap confidence interval of these new runs.
3. Reads the historical baseline mean from `/home/user/baseline_mean.txt`.
4. Performs a statistical hypothesis comparison using standard bash utilities (like `awk` or `bc`):
   - If the baseline mean strictly falls *between* the LOWER and UPPER bounds of the bootstrap CI, write the word `PASS` to `/home/user/regression_result.log`.
   - If the baseline mean is outside or exactly on the boundaries of the CI, write `FAIL` to `/home/user/regression_result.log`.

Make sure your script is executable (`chmod +x`). Do not manually run the script; just create it perfectly, as our CI pipeline will execute it. Ensure all temporary and output files are created in `/home/user`.