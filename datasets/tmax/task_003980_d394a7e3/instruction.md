You are a performance engineer working on a distributed scientific simulation. Your team noticed that the application produces slightly different final results depending on the number of MPI processes used. This non-reproducibility is suspected to be caused by floating-point addition non-associativity during parallel reductions.

I have placed a simplified version of the simulation at `/home/user/reduce_sim.py`. It takes a single integer argument as a random seed, generates a large array of floats (with varying magnitudes to exacerbate floating-point errors), distributes the array across MPI ranks, performs a local sum, and uses `MPI.SUM` to reduce the total to rank 0.

Your task is to analyze this non-reproducibility, quantify it, visualize it, and fix the code.

Perform the following steps:
1. **Environment Setup**: Install any necessary dependencies to run MPI applications in Python (`mpi4py`), as well as `scipy` and `matplotlib` for analysis.
2. **Experimentation**: Write a Python script `/home/user/analyze.py` that runs `/home/user/reduce_sim.py` across 50 different seeds (integers 1 through 50 inclusive). For each seed, run the simulation twice: once with 1 MPI process (`mpirun -n 1`) and once with 4 MPI processes (`mpirun -n 4`). 
3. **Statistical Analysis**: In `/home/user/analyze.py`, calculate the 1-D Wasserstein distance (using `scipy.stats.wasserstein_distance`) between the distribution of the 50 results from the 1-process runs and the distribution of the 50 results from the 4-process runs. Save this single floating-point number to `/home/user/metric.txt`.
4. **Visualization**: Have `/home/user/analyze.py` generate a plot named `/home/user/visualization.png` that overlays the histograms (or KDEs) of the 1-process results and 4-process results.
5. **Fix the Simulation**: Create a new file `/home/user/fix_sim.py` based on `reduce_sim.py`. Modify the communication/reduction logic so that the final summed result is *exactly identical* (bitwise) regardless of whether it is run with 1, 2, 4, or 8 processes, without changing the mathematical intent of summing the global array. (Hint: Gathering all data to the root rank and using Python's `math.fsum` or a deterministic sum on the gathered array is acceptable for this task).

Ensure that:
- `/home/user/metric.txt` contains only the computed Wasserstein distance.
- `/home/user/fix_sim.py` uses `mpi4py` and handles the exact same inputs (seed argument) but produces process-count-invariant results.