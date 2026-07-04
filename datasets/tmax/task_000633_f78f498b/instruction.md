You are a performance engineer profiling a scientific application. One of the core routines involves matrix factorization, but it frequently fails in production due to near-singular inputs. 

We have isolated the factorization routine into a script at `/home/user/factorize.py`. It accepts a single integer seed as an argument, generates a matrix, computes its condition number, and attempts to factorize it. It prints either `SUCCESS <condition_number>` or `FAIL <condition_number>` to standard output.

Your task is to analyze the statistical difference between the matrices that succeed and those that fail.

Perform the following steps:
1. Use standard bash CLI tools (like `seq` and `xargs`) to run `/home/user/factorize.py` for all integer seeds from `1` to `1000` inclusive. You must run these in parallel using 4 concurrent processes (e.g., using `xargs -P 4`).
2. Capture the combined standard output of all these runs into a single file at `/home/user/all_runs.txt`.
3. Write a Python script at `/home/user/distance.py` that reads `/home/user/all_runs.txt` and separates the condition numbers into two sets: one for `SUCCESS` runs and one for `FAIL` runs.
4. Your Python script must compute the 1D Wasserstein distance between the condition number distributions of the successful vs. failed runs. Use `scipy.stats.wasserstein_distance` for this calculation.
5. The script should save only the final Wasserstein distance, rounded to 2 decimal places, into `/home/user/result.txt`.

Ensure your Python script relies only on standard libraries, `numpy`, and `scipy`.