I am tracking down a nasty floating-point regression in our Python codebase located at `/home/user/timeseries_proj`. This repository contains about 200 commits. 

The main script, `calc_var.py`, calculates the variance of a deterministically generated chaotic sequence based on a given float seed. We have a highly optimized, numerically stable reference implementation compiled as a stripped C binary located at `/app/ref_calc`. 

Sometime in the last 200 commits, a developer "optimized" the Python variance calculation, which unfortunately introduced catastrophic cancellation or severe floating-point precision loss. The output of `calc_var.py` now significantly deviates from `/app/ref_calc` for large sequences.

Your tasks are to:
1. Use git bisection (or any other method) to find the exact commit hash that introduced this precision regression. Write the full 40-character commit hash to `/home/user/bad_commit.txt`.
2. Inspect the mathematical error introduced in that commit.
3. Fix the floating-point precision issue in the **latest** version (HEAD) of `calc_var.py` without reverting the performance optimizations (e.g., do not use the slow `decimal` module, and keep it a single-pass or highly efficient algorithm if possible). 
4. Save your corrected script to `/home/user/fixed_calc_var.py`.

Your `fixed_calc_var.py` must accept a single float seed as a command-line argument and print the variance to standard output, exactly matching the interface of the original script and the reference binary.

The automated verification will test your `fixed_calc_var.py` against `/app/ref_calc` on several hidden seeds to ensure the output matches within a very strict numerical threshold.