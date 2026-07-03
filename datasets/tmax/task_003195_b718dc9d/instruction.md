You are acting as a performance engineer profiling a new MPI-based numerical simulation. You have collected latency distribution data for the main simulation loop at different scales (1, 2, 4, and 8 MPI ranks). 

The data is stored in `/home/user/profiling_data/` as `rank_1.csv`, `rank_2.csv`, `rank_4.csv`, and `rank_8.csv`. Each file contains a single column of latency measurements (in milliseconds) for the simulation loop across many iterations.

Your task is to write and execute a Python script at `/home/user/analyze.py` that performs the following analysis:
1. Calculates the mean latency for each scaling configuration (N=1, 2, 4, 8).
2. Fits Amdahl's Law to these mean latencies to estimate the parallelizable fraction ($P$) of the code. Amdahl's Law for execution time is: $T(N) = T(1) \times ((1 - P) + P / N)$.
3. Computes the 1D Wasserstein distance between the raw latency distributions of the N=1 run and the N=8 run to quantify the shift in performance variance and distribution.
4. Outputs the estimated parallel fraction and the Wasserstein distance to a JSON file at `/home/user/results.json` with the exact keys `parallel_fraction` (float) and `wasserstein_distance` (float).

Ensure your script handles standard numerical stability practices and uses `scipy.stats` and `scipy.optimize`. 
Run your script to produce the final `results.json`.